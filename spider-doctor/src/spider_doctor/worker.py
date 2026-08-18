from __future__ import annotations

import json
import re
from datetime import timedelta
from pathlib import Path
from typing import Protocol

from spider_doctor.models import DoctorResult, DoctorStatus, DoctorTask


class Repository(Protocol):
    def claim(self, worker_id: str, *, lease_for: timedelta) -> DoctorTask | None: ...
    def complete(self, task_id: str, lease_token: str, status: DoctorStatus, result: dict) -> bool: ...
    def fail_attempt(
        self,
        task_id: str,
        lease_token: str,
        error: str,
        *,
        attempts: int,
        max_attempts: int,
    ) -> DoctorStatus | None: ...


class EvidenceLoader(Protocol):
    def load(self, task: DoctorTask) -> dict: ...


class Workspace(Protocol):
    def prepare(self, task_id: str, release: str) -> Path: ...
    def validate_changes(self, workspace: Path, slug: str) -> list[str]: ...


class Launcher(Protocol):
    def run(self, task: DoctorTask, *, workspace: Path, task_file: Path, output_dir: Path) -> DoctorResult: ...


class DoctorWorker:
    def __init__(
        self,
        repository: Repository,
        evidence_loader: EvidenceLoader,
        workspace_manager: Workspace,
        launcher: Launcher,
        *,
        worker_id: str,
        task_root: Path,
        lease_for: timedelta = timedelta(minutes=30),
    ) -> None:
        self.repository = repository
        self.evidence_loader = evidence_loader
        self.workspace_manager = workspace_manager
        self.launcher = launcher
        self.worker_id = worker_id
        self.task_root = task_root.resolve()
        self.lease_for = lease_for

    def process_one(self) -> DoctorResult | None:
        task = self.repository.claim(self.worker_id, lease_for=self.lease_for)
        if task is None:
            return None
        if task.lease is None:
            raise RuntimeError("claimed Doctor task has no lease")

        try:
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

            result = self.launcher.run(
                task,
                workspace=workspace,
                task_file=task_file,
                output_dir=output_dir,
            )
            if result.status == DoctorStatus.FAILED:
                detail = "; ".join(result.errors) or result.summary
                raise RuntimeError(f"Hermes reported failure: {detail}")
            actual_changes = self.workspace_manager.validate_changes(workspace, task.slug)
            if result.status == DoctorStatus.AWAITING_REVIEW and not actual_changes:
                raise ValueError("Hermes reported a repair but produced no allowed changes")
            result.changed_files = actual_changes
            result_payload = result.model_dump(mode="json")
            if not self.repository.complete(
                task.id,
                task.lease.token,
                result.status,
                result_payload,
            ):
                raise RuntimeError("Doctor task lease was lost before completion")
            return result
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"[:4000]
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
                summary="Doctor attempt failed before producing a reviewable patch",
                errors=[error],
                metadata={"task_status": str(failure_status)},
            )
