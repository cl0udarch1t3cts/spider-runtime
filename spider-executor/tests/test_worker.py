
import mongomock

from spider_executor.models import (
    Artifact,
    Entry,
    ExecutionJob,
    FailureClass,
    JobStatus,
    RunnerResult,
    ScrapedRecord,
)
from spider_executor.service import MongoControlService
from spider_executor.worker import ExecutorWorker


class FakeRunner:
    def __init__(self, result: RunnerResult) -> None:
        self.result = result

    def run(self, slug: str, run_id: str) -> RunnerResult:
        return self.result


def successful_result() -> RunnerResult:
    return RunnerResult(
        exit_code=0,
        record=ScrapedRecord(
            slug="example",
            website="https://example.com",
            fields={"NAME": {"value": "Example", "source": "https://example.com"}},
        ),
        output_artifact=Artifact(key="runs/x/output.json", size_bytes=1, sha256="0" * 64),
    )


def make_service():
    client = mongomock.MongoClient()
    return MongoControlService(client.spider)


def test_worker_persists_successful_run_and_record() -> None:
    service = make_service()
    service.put_entry(
        Entry(
            slug="example",
            name="Example",
            website="https://example.com",
            validation={"required_fields": ["NAME"], "minimum_non_null_fields": 1},
        )
    )
    job = service.enqueue(ExecutionJob(slug="example", idempotency_key="one"))
    worker = ExecutorWorker(service, FakeRunner(successful_result()), worker_id="worker-1")

    run = worker.process_one()

    assert run is not None
    assert run.status == JobStatus.SUCCEEDED
    assert service.get_job(job.id).status == JobStatus.SUCCEEDED
    assert len(service.list_runs("example")) == 1
    assert service.get_record(run.record_id).fields["NAME"].value == "Example"
    assert service.doctor_task_count() == 0


def test_artifact_failure_is_recorded_without_doctor_task() -> None:
    class BrokenArtifacts:
        def put(self, key, content):
            raise OSError("disk full")

    service = make_service()
    service.put_entry(Entry(slug="example", name="Example", website="https://example.com"))
    service.enqueue(ExecutionJob(slug="example", idempotency_key="artifact-failure"))
    worker = ExecutorWorker(
        service,
        FakeRunner(successful_result()),
        worker_id="worker-1",
        artifacts=BrokenArtifacts(),
    )

    run = worker.process_one()

    assert run.status == JobStatus.FAILED
    assert run.failure_class.value == "UNKNOWN"
    assert service.get_job(run.job_id).status == JobStatus.FAILED
    assert service.doctor_task_count() == 0


def test_inactive_entry_does_not_run_or_create_doctor_task() -> None:
    service = make_service()
    service.put_entry(Entry(slug="example", name="Example", website="https://example.com", active=False))
    service.enqueue(ExecutionJob(slug="example", idempotency_key="inactive"))

    run = ExecutorWorker(service, FakeRunner(successful_result()), worker_id="worker-1").process_one()

    assert run.status == JobStatus.FAILED
    assert run.failure_class.value == "INACTIVE_ENTRY"
    assert service.doctor_task_count() == 0


def test_wrong_record_slug_is_identity_failure() -> None:
    service = make_service()
    service.put_entry(Entry(slug="example", name="Example", website="https://example.com"))
    result = successful_result()
    result.record.slug = "other"
    service.enqueue(ExecutionJob(slug="example", idempotency_key="wrong-slug"))

    run = ExecutorWorker(service, FakeRunner(result), worker_id="worker-1").process_one()

    assert run.status == JobStatus.FAILED
    assert run.failure_class.value == "IDENTITY_MISMATCH"
    assert service.doctor_task_count() == 1


def test_runner_network_failure_is_not_misclassified_as_release_mismatch() -> None:
    service = make_service()
    service.put_entry(
        Entry(
            slug="example",
            name="Example",
            website="https://example.com",
            scraper_release="expected-sha",
        )
    )
    result = successful_result()
    result.exit_code = 2
    result.scraper_release = None
    result.failure_class = FailureClass.NETWORK_TIMEOUT
    result.record.errors = ["isolated runner unavailable"]
    service.enqueue(ExecutionJob(slug="example", idempotency_key="runner-network"))

    run = ExecutorWorker(service, FakeRunner(result), worker_id="worker-1").process_one()

    assert run.failure_class.value == "NETWORK_TIMEOUT"
    assert service.doctor_task_count() == 0


def test_release_mismatch_fails_before_accepting_record() -> None:
    service = make_service()
    service.put_entry(
        Entry(
            slug="example",
            name="Example",
            website="https://example.com",
            scraper_release="expected-sha",
            validation={"required_fields": ["NAME"]},
        )
    )
    result = successful_result()
    result.scraper_release = "wrong-sha"
    service.enqueue(ExecutionJob(slug="example", idempotency_key="release"))

    run = ExecutorWorker(service, FakeRunner(result), worker_id="worker-1").process_one()

    assert run.status == JobStatus.FAILED
    assert run.failure_class.value == "IDENTITY_MISMATCH"
    assert service.doctor_task_count() == 1


def test_semantic_failure_creates_one_doctor_task() -> None:
    service = make_service()
    service.put_entry(
        Entry(
            slug="example",
            name="Example",
            website="https://example.com",
            validation={"required_fields": ["NAME"]},
        )
    )
    bad = successful_result()
    bad.record.fields["NAME"].value = None
    bad.record.fields["NAME"].source = None
    service.enqueue(ExecutionJob(slug="example", idempotency_key="bad-1"))
    service.enqueue(ExecutionJob(slug="example", idempotency_key="bad-2"))
    worker = ExecutorWorker(service, FakeRunner(bad), worker_id="worker-1")

    first = worker.process_one()
    second = worker.process_one()

    assert first.status == JobStatus.FAILED
    assert second.status == JobStatus.FAILED
    assert service.doctor_task_count() == 1
    task = service.db.doctor_tasks.find_one({"active_key": "example"})
    assert task["status"] == "queued"
    assert task["attempts"] == 0
    assert task["max_attempts"] == 2
    assert task["priority"] == 50
    assert task["available_at"] is not None
    assert task["lease"] is None


def test_new_failure_does_not_retarget_running_or_reviewable_doctor_task() -> None:
    service = make_service()
    service.put_entry(
        Entry(
            slug="example",
            name="Example",
            website="https://example.com",
            validation={"required_fields": ["NAME"]},
        )
    )
    bad = successful_result()
    bad.record.fields["NAME"].value = None
    bad.record.fields["NAME"].source = None
    service.enqueue(ExecutionJob(slug="example", idempotency_key="initial-failure"))
    worker = ExecutorWorker(service, FakeRunner(bad), worker_id="worker-1")
    initial = worker.process_one()
    service.db.doctor_tasks.update_one(
        {"active_key": "example"},
        {"$set": {"status": "awaiting_review"}},
    )
    service.enqueue(ExecutionJob(slug="example", idempotency_key="later-failure"))

    worker.process_one()

    task = service.db.doctor_tasks.find_one({"active_key": "example"})
    assert task["status"] == "awaiting_review"
    assert task["source_run_id"] == initial.id


def test_new_failure_does_not_retarget_queued_create_task() -> None:
    service = make_service()
    service.put_entry(
        Entry(
            slug="example",
            name="Example",
            website="https://example.com",
            validation={"required_fields": ["NAME"]},
        )
    )
    service.db.doctor_tasks.insert_one(
        {
            "_id": "create-task",
            "active_key": "example",
            "slug": "example",
            "type": "create",
            "status": "queued",
            "source_run_id": None,
            "failure_class": "NEW_SCRAPER",
            "errors": [],
            "request": {"name": "Example", "address": "Main Street 1"},
        }
    )
    bad = successful_result()
    bad.record.fields["NAME"].value = None
    bad.record.fields["NAME"].source = None
    service.enqueue(ExecutionJob(slug="example", idempotency_key="repair-failure"))

    ExecutorWorker(service, FakeRunner(bad), worker_id="worker-1").process_one()

    task = service.db.doctor_tasks.find_one({"_id": "create-task"})
    assert task["type"] == "create"
    assert task["source_run_id"] is None
    assert task["failure_class"] == "NEW_SCRAPER"
    assert task["errors"] == []
