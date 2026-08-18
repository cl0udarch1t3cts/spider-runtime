from datetime import UTC, datetime, timedelta
from pathlib import Path

from spider_doctor.models import DoctorResult, DoctorStatus, DoctorTask, Lease
from spider_doctor.worker import DoctorWorker


class FakeRepository:
    def __init__(self, task: DoctorTask) -> None:
        self.task = task
        self.completed = None
        self.failed = None

    def claim(self, worker_id: str, lease_for: timedelta):
        return self.task

    def complete(self, task_id, lease_token, status, result):
        self.completed = (task_id, lease_token, status, result)
        return True

    def fail_attempt(self, task_id, lease_token, error, **kwargs):
        self.failed = (task_id, lease_token, error)
        return DoctorStatus.QUEUED


class FakeEvidence:
    def load(self, task):
        return {"task": task.model_dump(mode="json", by_alias=True), "scraper_release": "a" * 40}


class FakeWorkspace:
    def __init__(self, root: Path) -> None:
        self.root = root

    def prepare(self, task_id, release):
        self.root.mkdir(parents=True)
        return self.root

    def validate_changes(self, workspace, slug):
        return [f"scrapers/{slug}/scrape.py"]


class FakeLauncher:
    def run(self, task, *, workspace, task_file, output_dir):
        return DoctorResult(
            status=DoctorStatus.AWAITING_REVIEW,
            summary="fixed",
            changed_files=["ignored-by-dispatcher"],
            tests=["pytest: passed"],
        )


def running_task() -> DoctorTask:
    return DoctorTask(
        _id="task-1",
        slug="example",
        status=DoctorStatus.RUNNING,
        attempts=1,
        source_run_id="job:1",
        failure_class="SCRAPER_EXCEPTION",
        lease=Lease(
            worker_id="doctor-1",
            token="token",
            expires_at=datetime.now(UTC) + timedelta(minutes=30),
        ),
    )


def test_process_one_launches_ephemeral_agent_and_fences_completion(tmp_path: Path) -> None:
    repository = FakeRepository(running_task())
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        FakeLauncher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.AWAITING_REVIEW
    assert result.changed_files == ["scrapers/example/scrape.py"]
    assert repository.completed[0:3] == ("task-1", "token", DoctorStatus.AWAITING_REVIEW)
    assert repository.completed[3]["changed_files"] == ["scrapers/example/scrape.py"]
    assert (tmp_path / "tasks" / "task-1" / "task.json").is_file()
    assert (tmp_path / "tasks" / "task-1" / "result-schema.json").is_file()


def test_process_one_returns_none_when_queue_is_empty(tmp_path: Path) -> None:
    repository = FakeRepository(None)
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        FakeLauncher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
    )

    assert worker.process_one() is None


def test_operational_failure_is_fenced_and_requeued(tmp_path: Path) -> None:
    class BrokenEvidence:
        def load(self, task):
            raise OSError("temporary storage failure")

    repository = FakeRepository(running_task())
    worker = DoctorWorker(
        repository,
        BrokenEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        FakeLauncher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.FAILED
    assert "temporary storage failure" in result.errors[0]
    assert repository.failed[0:2] == ("task-1", "token")


def test_structured_agent_failure_uses_bounded_retry_path(tmp_path: Path) -> None:
    class FailedLauncher:
        def run(self, task, *, workspace, task_file, output_dir):
            return DoctorResult(
                status=DoctorStatus.FAILED,
                summary="could not reproduce",
                errors=["network unavailable"],
            )

    repository = FakeRepository(running_task())
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        FailedLauncher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.FAILED
    assert repository.completed is None
    assert repository.failed[0:2] == ("task-1", "token")
