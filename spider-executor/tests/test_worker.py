
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

RELEASE = "a" * 40


class FakeRunner:
    def __init__(self, result: RunnerResult) -> None:
        self.result = result

    def run(self, entry_id: str, run_id: str) -> RunnerResult:
        return self.result


def successful_result() -> RunnerResult:
    return RunnerResult(
        exit_code=0,
        record=ScrapedRecord(
            entry_id="example",
            website="https://example.com",
            fields={"NAME": {"value": "Example", "source": "https://example.com"}},
        ),
        output_artifact=Artifact(key="runs/x/output.json", size_bytes=1, sha256="0" * 64),
        scraper_release=RELEASE,
    )


def make_service():
    client = mongomock.MongoClient()
    service = MongoControlService(client.spider)
    service.db.runtime_state.insert_one(
        {"_id": "activated_entry", "entry_id": "example", "scraper_release": RELEASE}
    )
    return service


def activated_entry(**overrides) -> Entry:
    data = {
        "entry_id": "example",
        "businessname": "Example",
        "address": "Bern",
        "scraper_release": RELEASE,
    }
    data.update(overrides)
    return Entry(**data)


def test_worker_persists_successful_run_and_record() -> None:
    service = make_service()
    service.put_entry(
        activated_entry(
            website="https://example.com",
            validation={"required_fields": ["NAME"], "minimum_non_null_fields": 1},
        )
    )
    job = service.enqueue(ExecutionJob(entry_id="example", idempotency_key="one"))
    worker = ExecutorWorker(service, FakeRunner(successful_result()), worker_id="worker-1")

    run = worker.process_one()

    assert run is not None
    assert run.status == JobStatus.SUCCEEDED
    assert service.get_job(job.id).status == JobStatus.SUCCEEDED
    assert len(service.list_runs("example")) == 1
    assert service.get_record(run.record_id).fields["NAME"].value == "Example"
    assert service.doctor_task_count() == 0


def test_worker_persists_bounded_stderr_log_tail_on_success_and_failure() -> None:
    service = make_service()
    service.put_entry(
        activated_entry(
            website="https://example.com",
            validation={"required_fields": ["NAME"], "minimum_non_null_fields": 1},
        )
    )
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="one"))
    result = successful_result()
    result.stderr = "warning: slow fetch\n" + ("x" * 20_000)
    worker = ExecutorWorker(service, FakeRunner(result), worker_id="worker-1")

    run = worker.process_one()

    stored = service.db.execution_runs.find_one({"_id": run.id})
    assert stored["log_tail"] == result.stderr[-16_384:]

    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="two"))
    failing = successful_result()
    failing.exit_code = 3
    failing.stderr = "Traceback: boom"
    failing.record.errors = ["Traceback: boom"]
    failed_run = ExecutorWorker(service, FakeRunner(failing), worker_id="worker-1").process_one()

    stored = service.db.execution_runs.find_one({"_id": failed_run.id})
    assert stored["log_tail"] == "Traceback: boom"


def test_post_doctor_handoff_job_executes_registered_entry_without_website() -> None:
    release = "a" * 40
    service = MongoControlService(
        mongomock.MongoClient().spider,
        release_provider=lambda: "b" * 40,
    )
    registration = service.register("example", "Example", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": release}}},
    )
    service.consume_doctor_handoff(registration["task_id"])
    result = successful_result()
    result.scraper_release = release

    run = ExecutorWorker(service, FakeRunner(result), worker_id="worker-1").process_one()

    assert run is not None
    assert run.status == JobStatus.SUCCEEDED
    assert service.doctor_task_count() == 1


def test_worker_rejects_job_for_non_active_prototype_entry_without_doctor_task() -> None:
    service = make_service()
    service.put_entry(
        Entry(entry_id="other", businessname="Other", address="Zurich", scraper_release=RELEASE)
    )
    service.jobs.enqueue(
        ExecutionJob(entry_id="other", idempotency_key="legacy-other", scraper_release=RELEASE)
    )

    run = ExecutorWorker(service, FakeRunner(successful_result()), worker_id="worker-1").process_one()

    assert run is not None
    assert run.status == JobStatus.FAILED
    assert run.failure_class == FailureClass.INACTIVE_ENTRY
    assert service.doctor_task_count() == 0


def test_worker_rejects_queued_job_before_release_activation() -> None:
    service = make_service()
    service.put_entry(
        Entry(entry_id="example", businessname="Example", address="Bern", website="https://example.com")
    )
    service.jobs.enqueue(ExecutionJob(entry_id="example", idempotency_key="legacy-bypass"))

    run = ExecutorWorker(service, FakeRunner(successful_result()), worker_id="worker-1").process_one()

    assert run is not None
    assert run.status == JobStatus.FAILED
    assert run.failure_class == FailureClass.INACTIVE_ENTRY
    assert run.errors == ["entry 'example' has no activated scraper release"]
    assert service.doctor_task_count() == 0


def test_artifact_failure_is_recorded_without_doctor_task() -> None:
    class BrokenArtifacts:
        def put(self, key, content):
            raise OSError("disk full")

    service = make_service()
    service.put_entry(activated_entry(website="https://example.com"))
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="artifact-failure"))
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
    service.put_entry(activated_entry(website="https://example.com", active=False))
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="inactive"))

    run = ExecutorWorker(service, FakeRunner(successful_result()), worker_id="worker-1").process_one()

    assert run.status == JobStatus.FAILED
    assert run.failure_class.value == "INACTIVE_ENTRY"
    assert service.doctor_task_count() == 0


def test_successful_run_backfills_missing_entry_website_from_record() -> None:
    service = make_service()
    service.put_entry(activated_entry(website=None))
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="one"))

    run = ExecutorWorker(
        service, FakeRunner(successful_result()), worker_id="worker-1"
    ).process_one()

    assert run.status == JobStatus.SUCCEEDED
    assert service.get_entry("example").website == "https://example.com"


def test_successful_run_never_overwrites_an_existing_entry_website() -> None:
    service = make_service()
    service.put_entry(activated_entry(website="https://registered.example"))
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="one"))

    ExecutorWorker(service, FakeRunner(successful_result()), worker_id="worker-1").process_one()

    assert service.get_entry("example").website == "https://registered.example"


def test_failed_run_does_not_auto_refer_to_doctor_while_suspended() -> None:
    # Operator policy: automatic Doctor care is suspended; broken scrapes
    # are referred manually via request_repair until further notice.
    service = make_service()
    service.put_entry(activated_entry(website="https://example.com"))
    result = successful_result()
    result.record.entry_id = "other"
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="suspended"))

    run = ExecutorWorker(service, FakeRunner(result), worker_id="worker-1").process_one()

    assert run.status == JobStatus.FAILED
    assert service.doctor_task_count() == 0
    assert service.request_repair(run.id)["status"] == "queued"
    assert service.doctor_task_count() == 1


def test_wrong_record_entry_id_is_identity_failure() -> None:
    service = make_service()
    service.set_auto_repair(True)
    service.put_entry(activated_entry(website="https://example.com"))
    result = successful_result()
    result.record.entry_id = "other"
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="wrong-entry_id"))

    run = ExecutorWorker(service, FakeRunner(result), worker_id="worker-1").process_one()

    assert run.status == JobStatus.FAILED
    assert run.failure_class.value == "IDENTITY_MISMATCH"
    assert service.doctor_task_count() == 1


def test_runner_network_failure_is_not_misclassified_as_release_mismatch() -> None:
    service = make_service()
    service.put_entry(
        activated_entry(
            website="https://example.com",
            scraper_release="expected-sha",
        )
    )
    service.db.runtime_state.replace_one(
        {"_id": "activated_entry"},
        {
            "_id": "activated_entry",
            "entry_id": "example",
            "scraper_release": "expected-sha",
        },
    )
    result = successful_result()
    result.exit_code = 2
    result.scraper_release = None
    result.failure_class = FailureClass.NETWORK_TIMEOUT
    result.record.errors = ["isolated runner unavailable"]
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="runner-network"))

    run = ExecutorWorker(service, FakeRunner(result), worker_id="worker-1").process_one()

    assert run.failure_class.value == "NETWORK_TIMEOUT"
    assert service.doctor_task_count() == 0


def test_release_mismatch_fails_before_accepting_record() -> None:
    service = make_service()
    service.put_entry(
        activated_entry(
            website="https://example.com",
            scraper_release="expected-sha",
            validation={"required_fields": ["NAME"]},
        )
    )
    service.db.runtime_state.replace_one(
        {"_id": "activated_entry"},
        {
            "_id": "activated_entry",
            "entry_id": "example",
            "scraper_release": "expected-sha",
        },
    )
    result = successful_result()
    result.scraper_release = "wrong-sha"
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="release"))

    run = ExecutorWorker(service, FakeRunner(result), worker_id="worker-1").process_one()

    assert run.status == JobStatus.FAILED
    assert run.failure_class.value == "RELEASE_MISMATCH"
    assert service.doctor_task_count() == 0


def test_semantic_failure_creates_one_doctor_task() -> None:
    service = make_service()
    service.set_auto_repair(True)
    service.put_entry(
        activated_entry(
            website="https://example.com",
            validation={"required_fields": ["NAME"]},
        )
    )
    bad = successful_result()
    bad.record.fields["NAME"].value = None
    bad.record.fields["NAME"].source = None
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="bad-1"))
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="bad-2"))
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
    service.set_auto_repair(True)
    service.put_entry(
        activated_entry(
            website="https://example.com",
            validation={"required_fields": ["NAME"]},
        )
    )
    bad = successful_result()
    bad.record.fields["NAME"].value = None
    bad.record.fields["NAME"].source = None
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="initial-failure"))
    worker = ExecutorWorker(service, FakeRunner(bad), worker_id="worker-1")
    initial = worker.process_one()
    service.db.doctor_tasks.update_one(
        {"active_key": "example"},
        {"$set": {"status": "awaiting_review"}},
    )
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="later-failure"))

    worker.process_one()

    task = service.db.doctor_tasks.find_one({"active_key": "example"})
    assert task["status"] == "awaiting_review"
    assert task["source_run_id"] == initial.id


def test_new_failure_does_not_retarget_queued_create_task() -> None:
    service = make_service()
    service.put_entry(
        activated_entry(
            website="https://example.com",
            validation={"required_fields": ["NAME"]},
        )
    )
    service.db.doctor_tasks.insert_one(
        {
            "_id": "create-task",
            "active_key": "example",
            "entry_id": "example",
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
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="repair-failure"))

    ExecutorWorker(service, FakeRunner(bad), worker_id="worker-1").process_one()

    task = service.db.doctor_tasks.find_one({"_id": "create-task"})
    assert task["type"] == "create"
    assert task["source_run_id"] is None
    assert task["failure_class"] == "NEW_SCRAPER"
    assert task["errors"] == []


def test_worker_accepts_run_from_descendant_release_and_records_actual_sha() -> None:
    # The shared spider-scripts checkout only moves forward; a run may execute
    # at a newer commit that contains the entry's pinned activation commit.
    newer = "b" * 40
    service = make_service()
    service.put_entry(
        activated_entry(
            website="https://example.com",
            validation={"required_fields": ["NAME"], "minimum_non_null_fields": 1},
        )
    )
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="descendant"))
    result = successful_result()
    result.scraper_release = newer
    checked = []

    def release_contains(ancestor: str, descendant: str) -> bool:
        checked.append((ancestor, descendant))
        return (ancestor, descendant) == (RELEASE, newer)

    worker = ExecutorWorker(
        service,
        FakeRunner(result),
        worker_id="worker-1",
        release_contains=release_contains,
    )

    run = worker.process_one()

    assert run.status == JobStatus.SUCCEEDED
    assert run.scraper_release == newer
    assert checked == [(RELEASE, newer)]


def test_worker_still_rejects_unrelated_release_with_lineage_check() -> None:
    service = make_service()
    service.put_entry(activated_entry(website="https://example.com"))
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="unrelated"))
    result = successful_result()
    result.scraper_release = "c" * 40

    worker = ExecutorWorker(
        service,
        FakeRunner(result),
        worker_id="worker-1",
        release_contains=lambda ancestor, descendant: False,
    )

    run = worker.process_one()

    assert run.status == JobStatus.FAILED
    assert run.failure_class == FailureClass.RELEASE_MISMATCH
