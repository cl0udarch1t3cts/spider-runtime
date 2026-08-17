from __future__ import annotations

import json
from typing import Protocol
from urllib.parse import urlparse

from spider_executor.artifacts import LocalArtifactStore
from spider_executor.failure import classify_runner_failure
from spider_executor.models import ExecutionRun, FailureClass, JobStatus, RunnerResult
from spider_executor.validation import RecordExpectations, validate_record


class Runner(Protocol):
    def run(self, slug: str, run_id: str) -> RunnerResult: ...


class ExecutorWorker:
    def __init__(
        self,
        service,
        runner: Runner,
        *,
        worker_id: str,
        artifacts: LocalArtifactStore | None = None,
    ) -> None:
        self.service = service
        self.runner = runner
        self.worker_id = worker_id
        self.artifacts = artifacts

    def process_one(self) -> ExecutionRun | None:
        job = self.service.claim(self.worker_id)
        if job is None:
            return None
        run_id = f"{job.id}:{job.attempts}"
        run = ExecutionRun(
            id=run_id,
            job_id=job.id,
            slug=job.slug,
            scraper_release=job.scraper_release,
            status=JobStatus.RUNNING,
        )
        self.service.save_run(run)
        entry = self.service.get_entry(job.slug)
        if entry is None:
            errors = [f"entry {job.slug!r} is not registered"]
            return self._fail(job.id, job.lease.token, run, FailureClass.OUTPUT_SCHEMA_FAILURE, errors)
        if not entry.active:
            return self._fail(
                job.id,
                job.lease.token,
                run,
                FailureClass.INACTIVE_ENTRY,
                [f"entry {job.slug!r} is inactive"],
            )

        result = self.runner.run(job.slug, run_id)
        if self.artifacts is not None:
            try:
                content = json.dumps(result.record.model_dump(mode="json"), indent=2).encode()
                result.output_artifact = self.artifacts.put(f"runs/{run_id}/output.json", content)
            except (OSError, TypeError, ValueError) as exc:
                return self._fail(
                    job.id,
                    job.lease.token,
                    run,
                    FailureClass.UNKNOWN,
                    [f"artifact persistence failed: {exc}"],
                )
        run.scraper_release = result.scraper_release
        if result.failure_class is not None:
            errors = result.record.errors or [result.stderr or f"runner exited {result.exit_code}"]
            return self._fail(job.id, job.lease.token, run, result.failure_class, errors)
        if result.record.slug != job.slug:
            return self._fail(
                job.id,
                job.lease.token,
                run,
                FailureClass.IDENTITY_MISMATCH,
                [f"record slug mismatch: expected {job.slug}, got {result.record.slug}"],
            )
        if entry.scraper_release and result.scraper_release != entry.scraper_release:
            return self._fail(
                job.id,
                job.lease.token,
                run,
                FailureClass.IDENTITY_MISMATCH,
                [
                    (
                        f"scraper release mismatch: expected {entry.scraper_release}, "
                        f"got {result.scraper_release or 'unknown'}"
                    )
                ],
            )
        expectation_data = entry.validation.model_dump()
        if not expectation_data["allowed_source_hosts"]:
            host = urlparse(entry.website).hostname
            expectation_data["allowed_source_hosts"] = [host] if host else []
        expectations = RecordExpectations.model_validate(expectation_data)
        if result.exit_code != 0:
            errors = result.record.errors or [result.stderr or f"runner exited {result.exit_code}"]
            return self._fail(
                job.id,
                job.lease.token,
                run,
                classify_runner_failure("\n".join(errors)),
                errors,
            )
        validation = validate_record(result.record, expectations)
        if not validation.valid:
            return self._fail(
                job.id,
                job.lease.token,
                run,
                FailureClass.SEMANTIC_VALIDATION_FAILURE,
                validation.errors,
            )

        completed = self.service.complete_success(job, run, result.record, result.output_artifact)
        if not completed:
            run.status = JobStatus.FAILED
            run.failure_class = FailureClass.UNKNOWN
            run.errors = ["lease was lost before completion"]
        return run

    def _fail(
        self,
        job_id: str,
        lease_token: str,
        run: ExecutionRun,
        failure: FailureClass,
        errors: list[str],
    ) -> ExecutionRun:
        job = self.service.get_job(job_id)
        if job is None or job.lease is None or job.lease.token != lease_token:
            run.status = JobStatus.FAILED
            run.failure_class = FailureClass.UNKNOWN
            run.errors = ["lease was lost before failure completion"]
            return run
        self.service.complete_failure(job, run, failure, errors)
        return run
