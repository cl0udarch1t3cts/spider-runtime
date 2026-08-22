from datetime import UTC, datetime, timedelta
from pathlib import Path

from spider_doctor.models import DoctorResult, DoctorStatus, DoctorTask, Lease
from spider_doctor.worker import DoctorWorker


class FakeRepository:
    def __init__(self, task: DoctorTask) -> None:
        self.task = task
        self.candidate = None
        self.published = None
        self.failed = None

    def claim(self, worker_id: str, lease_for: timedelta):
        return self.task

    def record_candidate(self, task_id, lease_token, candidate_sha, result):
        self.candidate = (task_id, lease_token, candidate_sha, result)
        return True

    def complete_publication(self, task_id, lease_token, candidate_sha):
        self.published = (task_id, lease_token, candidate_sha)
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

    def resume(self, task_id, candidate_sha):
        return self.root

    def validate_changes(self, workspace, entry_id):
        return [f"scrapers/{entry_id}/scrape.py"]


class FakeLauncher:
    def run(self, task, *, workspace, task_file, output_dir):
        return DoctorResult(
            status=DoctorStatus.AWAITING_REVIEW,
            summary="fixed",
            changed_files=["ignored-by-dispatcher"],
            tests=["pytest: passed"],
        )


class FakePublisher:
    candidate_sha = "c" * 40

    def create_candidate(self, workspace, validated_files, message):
        return self.candidate_sha

    def publish(self, workspace, candidate_sha):
        assert candidate_sha == self.candidate_sha
        return candidate_sha


def running_task() -> DoctorTask:
    return DoctorTask(
        _id="task-1",
        entry_id="example",
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
        FakePublisher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.AWAITING_REVIEW
    assert result.changed_files == ["scrapers/example/scrape.py"]
    assert repository.candidate[0:3] == ("task-1", "token", "c" * 40)
    assert repository.candidate[3]["changed_files"] == ["scrapers/example/scrape.py"]
    assert repository.published == ("task-1", "token", "c" * 40)
    assert (tmp_path / "tasks" / "task-1" / "task.json").is_file()
    assert (tmp_path / "tasks" / "task-1" / "result-schema.json").is_file()


def test_resume_records_rebased_sha_before_completing_publication(tmp_path: Path) -> None:
    class RebasingPublisher:
        def create_candidate(self, workspace, validated_files, message):
            raise AssertionError("resume must not create a new candidate")

        def publish(self, workspace, candidate_sha):
            assert candidate_sha == "c" * 40
            return "d" * 40

    task = running_task()
    task.candidate_sha = "c" * 40
    task.candidate_result = {"status": "awaiting_review", "summary": "fixed"}
    repository = FakeRepository(task)
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        FakeLauncher(),
        RebasingPublisher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.AWAITING_REVIEW
    assert repository.candidate[0:3] == ("task-1", "token", "d" * 40)
    assert repository.published == ("task-1", "token", "d" * 40)


def test_process_one_returns_none_when_queue_is_empty(tmp_path: Path) -> None:
    repository = FakeRepository(None)
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        FakeLauncher(),
        FakePublisher(),
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
        FakePublisher(),
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
        FakePublisher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.FAILED
    assert repository.candidate is None
    assert repository.failed[0:2] == ("task-1", "token")


def test_agent_result_schema_exposes_only_untrusted_terminal_statuses() -> None:
    schema = DoctorResult.model_json_schema()
    status_schema = schema["properties"]["status"]
    if "$ref" in status_schema:
        status_schema = schema["$defs"][status_schema["$ref"].rsplit("/", 1)[-1]]

    assert set(status_schema["enum"]) == {"awaiting_review", "failed"}
