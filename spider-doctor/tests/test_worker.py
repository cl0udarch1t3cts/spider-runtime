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
        self.no_website = None

    def resolve_no_website(self, task_id, lease_token, summary):
        self.no_website = (task_id, lease_token, summary)
        return True

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


def test_success_records_generation_durations_in_result_metadata(tmp_path: Path) -> None:
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

    worker.process_one()

    metadata = repository.candidate[3]["metadata"]
    assert metadata["hermes_seconds"] >= 0
    assert metadata["attempt_seconds"] >= metadata["hermes_seconds"]


def test_failure_error_carries_attempt_duration(tmp_path: Path) -> None:
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

    worker.process_one()

    assert "attempt_seconds=" in repository.failed[2]


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


def test_no_reliable_website_ends_the_task_without_retry(tmp_path: Path) -> None:
    class NoWebsiteLauncher:
        def run(self, task, *, workspace, task_file, output_dir):
            return DoctorResult(
                status=DoctorStatus.FAILED,
                summary="no official website for this business could be verified",
                resolution="no_reliable_website",
            )

    repository = FakeRepository(running_task())
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        NoWebsiteLauncher(),
        FakePublisher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.FAILED
    assert repository.no_website == (
        "task-1",
        "token",
        "no official website for this business could be verified",
    )
    # A terminal finding, not an error: the bounded-retry path is not used.
    assert repository.failed is None


def test_agent_result_schema_exposes_only_untrusted_terminal_statuses() -> None:
    schema = DoctorResult.model_json_schema()
    status_schema = schema["properties"]["status"]
    if "$ref" in status_schema:
        status_schema = schema["$defs"][status_schema["$ref"].rsplit("/", 1)[-1]]

    assert set(status_schema["enum"]) == {"awaiting_review", "failed"}


class FakeBudgetGate:
    def __init__(self, allowed: bool) -> None:
        self.allowed = allowed
        self.checks = 0

    def check(self):
        from spider_doctor.budget import BudgetDecision

        self.checks += 1
        return BudgetDecision(self.allowed, "usage 12.0% of 10.0% allowed via api")


class MustNotLaunch:
    def run(self, task, *, workspace, task_file, output_dir):
        raise AssertionError("Hermes must not be launched while over budget")


def test_budget_defer_releases_the_task_without_launching_hermes(tmp_path: Path) -> None:
    class ReleasingRepository(FakeRepository):
        def __init__(self, task):
            super().__init__(task)
            self.released = None

        def release(self, task_id, lease_token, *, retry_after):
            self.released = (task_id, lease_token, retry_after)
            return True

    repository = ReleasingRepository(running_task())
    gate = FakeBudgetGate(allowed=False)
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        MustNotLaunch(),
        FakePublisher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
        budget_gate=gate,
        budget_retry_after=timedelta(minutes=45),
    )

    result = worker.process_one()

    assert result is None
    assert gate.checks == 1
    assert repository.released == ("task-1", "token", timedelta(minutes=45))
    assert repository.failed is None
    assert repository.candidate is None


def test_budget_proceed_launches_hermes_normally(tmp_path: Path) -> None:
    repository = FakeRepository(running_task())
    gate = FakeBudgetGate(allowed=True)
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        FakeLauncher(),
        FakePublisher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
        budget_gate=gate,
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.AWAITING_REVIEW
    assert gate.checks == 1
    assert repository.published is not None


def test_candidate_publication_skips_the_budget_gate(tmp_path: Path) -> None:
    class MustNotCheck:
        def check(self):
            raise AssertionError("publication of a persisted candidate spends no budget")

    task = running_task()
    task.candidate_sha = "c" * 40
    task.candidate_result = {"status": "awaiting_review", "summary": "fixed"}
    repository = FakeRepository(task)
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        MustNotLaunch(),
        FakePublisher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
        budget_gate=MustNotCheck(),
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.AWAITING_REVIEW
    assert repository.published == ("task-1", "token", "c" * 40)


def test_pause_flag_stops_claiming_entirely(tmp_path: Path) -> None:
    class MustNotClaim(FakeRepository):
        def claim(self, worker_id, lease_for):
            raise AssertionError("paused Doctor must not claim tasks")

    worker = DoctorWorker(
        MustNotClaim(running_task()),
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        MustNotLaunch(),
        FakePublisher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
        pause_check=lambda: True,
    )

    assert worker.process_one() is None


def test_pause_check_false_processes_normally(tmp_path: Path) -> None:
    repository = FakeRepository(running_task())
    worker = DoctorWorker(
        repository,
        FakeEvidence(),
        FakeWorkspace(tmp_path / "workspace"),
        FakeLauncher(),
        FakePublisher(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
        pause_check=lambda: False,
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.AWAITING_REVIEW
    assert repository.published is not None
