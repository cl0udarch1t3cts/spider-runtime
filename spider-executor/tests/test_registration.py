from datetime import UTC, datetime

import mongomock
import pytest
from pydantic import ValidationError

from spider_executor.models import Entry, ExecutionJob
from spider_executor.service import MongoControlService


def test_registration_service_rejects_unsafe_or_unbounded_identity() -> None:
    service = MongoControlService(
        mongomock.MongoClient().spider,
        release_provider=lambda: "b" * 40,
    )

    with pytest.raises(ValidationError):
        service.register("../escape", "Example AG", "Bern")
    with pytest.raises(ValidationError):
        service.register("business-123", "x" * 257, "Bern")


@pytest.mark.parametrize(
    "entry_id",
    [
        "-6tlhQ5q6U9tq4xVLNAIkg",
        "_G66OOCKSeOjO2JWkr6aNA",
        "8_bWr7 3tjEHrLq2WsIpWHw",
        "31lzOvK_ _8nVc1PQNGaxpA",
    ],
)
def test_registration_accepts_base64url_style_upstream_ids(entry_id: str) -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    service.ensure_indexes()

    accepted = service.register(entry_id, "Example AG", "Bern")

    assert accepted["entry_id"] == entry_id
    assert service.db.entries.find_one({"_id": entry_id}) is not None


@pytest.mark.parametrize(
    "entry_id",
    [".hidden", "..", " leading-space", "trailing-space ", "a" * 129, ""],
)
def test_registration_rejects_dot_leading_and_space_edged_ids(entry_id: str) -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)

    with pytest.raises(ValidationError):
        service.register(entry_id, "Example AG", "Bern")


def test_register_upserts_entry_and_deduplicates_create_task() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    service.ensure_indexes()

    first = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": first["task_id"]},
        {
            "$set": {
                "attempts": 1,
                "available_at": "later",
                "last_error": "identity mismatch",
                "errors": ["identity mismatch"],
            }
        },
    )
    second = service.register("business-123", "Example AG Updated", "Zurich")

    assert first["task_id"] == second["task_id"]
    assert second == {
        "entry_id": "business-123",
        "task_id": first["task_id"],
        "status": "queued",
        "operation": "create",
    }
    entry = service.db.entries.find_one({"_id": "business-123"})
    assert entry is not None
    entry.pop("updated_at")
    entry.pop("created_at")
    assert entry == {
        "_id": "business-123",
        "entry_id": "business-123",
        "businessname": "Example AG Updated",
        "address": "Zurich",
    }
    tasks = list(service.db.doctor_tasks.find({"entry_id": "business-123", "type": "create"}))
    assert len(tasks) == 1
    assert tasks[0]["status"] == "queued"
    assert tasks[0]["active_key"] == "business-123"
    assert tasks[0]["base_release"] == "b" * 40
    assert tasks[0]["attempts"] == 0
    assert tasks[0]["lease"] is None
    assert tasks[0]["errors"] == []
    assert "last_error" not in tasks[0]
    assert tasks[0]["available_at"] != "later"
    assert "slug" not in tasks[0]


def test_identical_reregistration_does_not_reset_create_attempts() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    service.ensure_indexes()
    first = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": first["task_id"]},
        {"$set": {"attempts": 1, "last_error": "discovery failed"}},
    )

    second = service.register("business-123", "Example AG", "Bern")

    task = service.db.doctor_tasks.find_one({"_id": second["task_id"]})
    assert task is not None
    assert task["attempts"] == 1
    assert task["last_error"] == "discovery failed"


def test_registration_correction_fails_closed_while_task_is_running() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    service.ensure_indexes()
    first = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": first["task_id"]},
        {"$set": {"status": "running"}},
    )

    with pytest.raises(RuntimeError, match="non-queued create task"):
        service.register("business-123", "Corrected AG", "Zurich")

    entry = service.get_entry("business-123")
    assert entry is not None
    assert entry.businessname == "Example AG"
    assert entry.address == "Bern"


def test_execution_enqueue_fails_closed_for_entry_without_activation_record() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.put_entry(
        Entry(entry_id="business-1", businessname="First", address="Bern", scraper_release="a" * 40)
    )
    service.put_entry(
        Entry(entry_id="business-2", businessname="Second", address="Zurich", scraper_release="b" * 40)
    )
    service.db.runtime_state.insert_one(
        {"_id": "activated_entry", "entry_id": "business-1", "scraper_release": "a" * 40}
    )

    # business-1 is authorized by the legacy singleton activation record;
    # business-2 has a release on the entry but no activation, so it fails closed.
    assert service.enqueue(
        ExecutionJob(entry_id="business-1", idempotency_key="manual:1")
    ).scraper_release == "a" * 40
    with pytest.raises(RuntimeError, match="activated scraper release"):
        service.enqueue(ExecutionJob(entry_id="business-2", idempotency_key="manual:2"))


def test_execution_enqueue_rejects_entry_before_release_activation() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    service.register("business-123", "Example AG", "Bern")

    with pytest.raises(RuntimeError, match="activated scraper release"):
        service.enqueue(ExecutionJob(entry_id="business-123", idempotency_key="manual:1"))


def test_execution_enqueue_requires_durable_activation_not_only_entry_release() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.put_entry(
        Entry(
            entry_id="business-123",
            businessname="Example AG",
            address="Bern",
            scraper_release="a" * 40,
        )
    )

    with pytest.raises(RuntimeError, match="activated scraper release"):
        service.enqueue(ExecutionJob(entry_id="business-123", idempotency_key="manual:1"))


def test_registered_entry_is_available_to_executor_by_entry_id() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)

    service.register("business-123", "Example AG", "Bern")

    entry = service.get_entry("business-123")
    assert entry is not None
    assert entry.entry_id == "business-123"
    assert entry.businessname == "Example AG"
    assert entry.address == "Bern"
    assert entry.website is None


def test_repair_budget_persists_across_fresh_tasks_and_requires_human_review() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.put_entry(
        Entry(
            entry_id="example",
            businessname="Example",
            address="Bern",
            scraper_release="a" * 40,
        )
    )

    for sequence in (1, 2):
        service.ensure_doctor_task(
            "example",
            f"run-{sequence}",
            "SCRAPER_EXCEPTION",
            ["selector missing"],
        )
        task = service.db.doctor_tasks.find_one({"active_key": "example"})
        assert task["status"] == "queued"
        assert task["repair_sequence"] == sequence
        service.db.doctor_tasks.update_one(
            {"_id": task["_id"]},
            {"$set": {"status": "succeeded"}, "$unset": {"active_key": ""}},
        )

    service.ensure_doctor_task(
        "example",
        "run-3",
        "SCRAPER_EXCEPTION",
        ["still broken"],
    )

    review = service.db.doctor_tasks.find_one({"active_key": "example"})
    assert review["status"] == "human_review_required"
    assert review["source_run_id"] == "run-3"
    assert service.db.entries.find_one({"_id": "example"})["repair_attempts"] == 2


def test_scrape_all_enqueues_every_activated_entry_once_per_hour() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.put_entry(
        Entry(entry_id="ready", businessname="Ready", address="Bern", scraper_release="a" * 40)
    )
    service.db.runtime_state.insert_one(
        {"_id": "activated_entry:ready", "entry_id": "ready", "scraper_release": "a" * 40}
    )
    # Registered but never provisioned: must be skipped, not crash the sweep.
    service.put_entry(Entry(entry_id="bare", businessname="Bare", address="Bern"))

    first = service.enqueue_all(trigger="console")
    second = service.enqueue_all(trigger="console")

    assert first == {"enqueued": 1, "skipped": 1}
    # Same hour bucket: the sweep is idempotent, no duplicate jobs.
    assert second == {"enqueued": 1, "skipped": 1}
    assert service.db.execution_jobs.count_documents({"entry_id": "ready"}) == 1


def test_scrape_failing_enqueues_only_still_failing_entries() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    now = datetime.now(UTC)
    for entry_id in ("broken", "healthy"):
        service.put_entry(
            Entry(entry_id=entry_id, businessname=entry_id, address="Bern", scraper_release="a" * 40)
        )
        service.db.runtime_state.insert_one(
            {"_id": f"activated_entry:{entry_id}", "entry_id": entry_id, "scraper_release": "a" * 40}
        )
    service.db.execution_runs.insert_many(
        [
            {"_id": "b:1", "entry_id": "broken", "status": "failed",
             "failure_class": "SCRAPER_EXCEPTION", "started_at": now},
            {"_id": "h:1", "entry_id": "healthy", "status": "succeeded", "started_at": now},
        ]
    )

    first = service.enqueue_failing(trigger="console")
    second = service.enqueue_failing(trigger="console")

    assert first == {"enqueued": 1, "skipped": 0}
    assert second == {"enqueued": 1, "skipped": 0}
    assert service.db.execution_jobs.count_documents({"entry_id": "broken"}) == 1
    assert service.db.execution_jobs.count_documents({"entry_id": "healthy"}) == 0


def test_operator_can_request_repair_from_a_recorded_run() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.put_entry(
        Entry(entry_id="example", businessname="Example", address="Bern", scraper_release="a" * 40)
    )
    service.db.execution_runs.insert_one(
        {
            "_id": "job-1:1",
            "entry_id": "example",
            "status": "failed",
            "failure_class": "SCRAPER_EXCEPTION",
            "errors": ["selector missing"],
        }
    )

    outcome = service.request_repair("job-1:1")

    assert outcome is not None
    assert outcome["entry_id"] == "example"
    assert outcome["status"] == "queued"
    task = service.db.doctor_tasks.find_one({"active_key": "example"})
    assert task["type"] == "repair"
    assert task["source_run_id"] == "job-1:1"
    assert task["failure_class"] == "SCRAPER_EXCEPTION"
    # Repeating the request reuses the active task instead of duplicating it.
    assert service.request_repair("job-1:1")["task_id"] == task["_id"]
    assert service.db.doctor_tasks.count_documents({"entry_id": "example"}) == 1
    assert service.request_repair("missing") is None


def test_create_task_blocks_simultaneous_repair_for_the_same_entry() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    service.ensure_indexes()

    registration = service.register("business-123", "Example AG", "Bern")
    service.ensure_doctor_task(
        "business-123",
        "run-1",
        "SCRAPER_EXCEPTION",
        ["selector missing"],
    )

    tasks = list(service.db.doctor_tasks.find({"entry_id": "business-123"}))
    assert len(tasks) == 1
    assert tasks[0]["_id"] == registration["task_id"]
    assert tasks[0]["type"] == "create"
    assert tasks[0]["active_key"] == "business-123"
    assert tasks[0]["source_run_id"] is None
