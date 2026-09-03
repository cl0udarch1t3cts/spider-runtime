from __future__ import annotations

import json
import logging
import re
import threading
import time
from collections.abc import Callable
from datetime import timedelta
from pathlib import Path
from typing import Protocol

from spider_doctor.budget import BudgetDecision
from spider_doctor.model_policy import budget_fallback, resolve_model
from spider_doctor.models import DoctorResult, DoctorStatus, DoctorTask

logger = logging.getLogger(__name__)


class Repository(Protocol):
    def claim(self, worker_id: str, *, lease_for: timedelta) -> DoctorTask | None: ...
    def release(
        self, task_id: str, lease_token: str, *, retry_after: timedelta
    ) -> bool: ...
    def record_candidate(
        self, task_id: str, lease_token: str, candidate_sha: str, result: dict
    ) -> bool: ...
    def complete_publication(self, task_id: str, lease_token: str, candidate_sha: str) -> bool: ...
    def fail_attempt(
        self,
        task_id: str,
        lease_token: str,
        error: str,
        *,
        attempts: int,
        max_attempts: int,
    ) -> DoctorStatus | None: ...
    def record_model(self, task_id: str, lease_token: str, model: str) -> bool: ...
    def resolve_no_website(self, task_id: str, lease_token: str, summary: str) -> bool: ...


class EvidenceLoader(Protocol):
    def load(self, task: DoctorTask) -> dict: ...


class Workspace(Protocol):
    def prepare(self, task_id: str, release: str) -> Path: ...
    def resume(self, task_id: str, candidate_sha: str) -> Path: ...
    def validate_changes(self, workspace: Path, entry_id: str) -> list[str]: ...


class Launcher(Protocol):
    def reconcile_orphans(self) -> None: ...
    def run(
        self,
        task: DoctorTask,
        *,
        workspace: Path,
        task_file: Path,
        output_dir: Path,
        model: str | None = None,
        provider: str | None = None,
    ) -> DoctorResult: ...


class Publisher(Protocol):
    def create_candidate(self, workspace: Path, validated_files: list[str], message: str) -> str: ...
    def publish(self, workspace: Path, candidate_sha: str) -> None: ...


class BudgetGate(Protocol):
    def check(self) -> BudgetDecision: ...


class DoctorWorker:
    def __init__(
        self,
        repository: Repository,
        evidence_loader: EvidenceLoader,
        workspace_manager: Workspace,
        launcher: Launcher,
        publisher: Publisher,
        *,
        worker_id: str,
        task_root: Path,
        lease_for: timedelta = timedelta(minutes=30),
        budget_gate: BudgetGate | None = None,
        budget_retry_after: timedelta = timedelta(minutes=30),
        pause_check: Callable[[], bool] | None = None,
        model_policy: Callable[[], dict | None] | None = None,
        codex_model: str = "gpt-5.4",
    ) -> None:
        self.repository = repository
        self.evidence_loader = evidence_loader
        self.workspace_manager = workspace_manager
        self.launcher = launcher
        self.publisher = publisher
        self.worker_id = worker_id
        self.task_root = task_root.resolve()
        self.lease_for = lease_for
        self.budget_gate = budget_gate
        self.budget_retry_after = budget_retry_after
        # Serializes publication within this process: concurrent pushes to the
        # same branch would force one task through the rebase-and-requeue path.
        self._publish_lock = threading.Lock()
        self.pause_check = pause_check
        self._pause_logged = False
        self.model_policy = model_policy
        self.codex_model = codex_model

    def _policy_document(self) -> dict | None:
        if self.model_policy is None:
            return None
        try:
            return self.model_policy()
        except Exception as exc:  # noqa: BLE001 - a policy outage must not stall repairs
            logger.warning("model policy unavailable, using codex model: %s", exc)
            return None

    def _paused(self) -> bool:
        if self.pause_check is None:
            return False
        paused = self.pause_check()
        if paused and not self._pause_logged:
            logger.warning("Doctor is paused: no tasks are claimed and no LLM calls are made")
            self._pause_logged = True
        elif not paused and self._pause_logged:
            logger.info("Doctor is unpaused: resuming task processing")
            self._pause_logged = False
        return paused

    def process_one(self) -> DoctorResult | None:
        if self._paused():
            return None
        task = self.repository.claim(self.worker_id, lease_for=self.lease_for)
        if task is None:
            return None
        if task.lease is None:
            raise RuntimeError("claimed Doctor task has no lease")

        policy = self._policy_document()
        choice = resolve_model(
            policy, task_id=task.id, attempt=task.attempts, codex_model=self.codex_model
        )
        # Publishing an already-persisted candidate spends no subscription
        # budget, and non-codex models are not subscription-priced, so only a
        # fresh codex-routed Hermes launch consults the gate.
        if task.candidate_sha is None and self.budget_gate is not None and choice.budget_gated:
            decision = self.budget_gate.check()
            if not decision.allowed:
                fallback = budget_fallback(policy)
                if fallback and fallback != choice.model:
                    logger.warning(
                        "Doctor budget fallback task=%s: %s -> %s (%s)",
                        task.id,
                        choice.model,
                        fallback,
                        decision.detail,
                    )
                    choice = resolve_model(
                        {"default_model": fallback},
                        task_id=task.id,
                        attempt=task.attempts,
                        codex_model=self.codex_model,
                    )
                else:
                    released = self.repository.release(
                        task.id, task.lease.token, retry_after=self.budget_retry_after
                    )
                    logger.warning(
                        "Doctor budget defer task=%s retry_in=%s released=%s: %s",
                        task.id,
                        self.budget_retry_after,
                        released,
                        decision.detail,
                    )
                    return None
            else:
                logger.info("Doctor budget proceed task=%s: %s", task.id, decision.detail)
        logger.info(
            "Doctor model task=%s attempt=%s model=%s provider=%s (%s)",
            task.id,
            task.attempts,
            choice.model,
            choice.provider,
            choice.reason,
        )
        self.repository.record_model(task.id, task.lease.token, choice.model)

        attempt_started = time.monotonic()
        try:
            if task.candidate_sha:
                workspace = self.workspace_manager.resume(task.id, task.candidate_sha)
                payload = task.candidate_result or {}
                with self._publish_lock:
                    published_sha = self.publisher.publish(workspace, task.candidate_sha)
                    if published_sha != task.candidate_sha and not self.repository.record_candidate(
                        task.id,
                        task.lease.token,
                        published_sha,
                        payload,
                    ):
                        raise RuntimeError("Doctor task lease was lost before candidate persistence")
                    if not self.repository.complete_publication(
                        task.id, task.lease.token, published_sha
                    ):
                        raise RuntimeError("Doctor task lease was lost before publication completion")
                return DoctorResult.model_validate(payload)

            evidence = self.evidence_loader.load(task)
            release = evidence["scraper_release"]
            workspace = self.workspace_manager.prepare(task.id, release)
            safe_id = re.sub(r"[^A-Za-z0-9_.-]", "-", task.id).strip("-.")
            task_dir = self.task_root / safe_id
            output_dir = task_dir / "result"
            output_dir.mkdir(parents=True, exist_ok=True)
            task_file = task_dir / "task.json"
            evidence_text = json.dumps(evidence, indent=2, sort_keys=True)
            if len(evidence_text.encode("utf-8")) > 1024 * 1024:
                raise ValueError("Doctor task evidence exceeds the 1 MiB limit")
            task_file.write_text(evidence_text)
            (task_dir / "result-schema.json").write_text(
                json.dumps(DoctorResult.model_json_schema(), indent=2, sort_keys=True)
            )

            hermes_started = time.monotonic()
            result = self.launcher.run(
                task,
                workspace=workspace,
                task_file=task_file,
                output_dir=output_dir,
                model=choice.model,
                provider=choice.provider,
            )
            result.metadata = {
                **result.metadata,
                "hermes_seconds": round(time.monotonic() - hermes_started, 1),
                "model": choice.model,
            }
            if result.status == DoctorStatus.FAILED and result.resolution == "no_reliable_website":
                # A finding, not a failure: end the task terminally without
                # consuming retry budget.
                if not self.repository.resolve_no_website(
                    task.id, task.lease.token, result.summary
                ):
                    raise RuntimeError("Doctor task lease was lost before no-website resolution")
                logger.info(
                    "Doctor task=%s resolved terminally: no reliable website (%s)",
                    task.id,
                    result.summary[:200],
                )
                return result
            if result.status == DoctorStatus.FAILED:
                detail = "; ".join(result.errors) or result.summary
                raise RuntimeError(f"Hermes reported failure: {detail}")
            actual_changes = self.workspace_manager.validate_changes(workspace, task.entry_id)
            if not actual_changes:
                raise ValueError("Hermes reported a repair but produced no allowed changes")
            result.changed_files = actual_changes
            result.metadata = {
                **result.metadata,
                "attempt_seconds": round(time.monotonic() - attempt_started, 1),
            }
            logger.info(
                "Doctor task=%s generation timing hermes_seconds=%s attempt_seconds=%s",
                task.id,
                result.metadata["hermes_seconds"],
                result.metadata["attempt_seconds"],
            )
            result_payload = result.model_dump(mode="json")
            with self._publish_lock:
                candidate_sha = self.publisher.create_candidate(
                    workspace,
                    actual_changes,
                    f"Doctor {task.type} {task.entry_id}",
                )
                if not self.repository.record_candidate(
                    task.id,
                    task.lease.token,
                    candidate_sha,
                    result_payload,
                ):
                    raise RuntimeError("Doctor task lease was lost before candidate persistence")
                published_sha = self.publisher.publish(workspace, candidate_sha)
                if published_sha != candidate_sha and not self.repository.record_candidate(
                    task.id,
                    task.lease.token,
                    published_sha,
                    result_payload,
                ):
                    raise RuntimeError("Doctor task lease was lost before candidate persistence")
                if not self.repository.complete_publication(
                    task.id, task.lease.token, published_sha
                ):
                    raise RuntimeError("Doctor task lease was lost before publication completion")
            return result
        except Exception as exc:
            attempt_seconds = round(time.monotonic() - attempt_started, 1)
            error = f"{type(exc).__name__}: {exc}"[:4000]
            error += f" (attempt_seconds={attempt_seconds})"
            failure_status = self.repository.fail_attempt(
                task.id,
                task.lease.token,
                error,
                attempts=task.attempts,
                max_attempts=task.max_attempts,
            )
            if failure_status is None:
                raise RuntimeError("Doctor task lease was lost while recording failure") from exc
            return DoctorResult(
                status=DoctorStatus.FAILED,
                summary="Doctor attempt failed before publishing a verified patch",
                errors=[error],
                metadata={"task_status": str(failure_status)},
            )
