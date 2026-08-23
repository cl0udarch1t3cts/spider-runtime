import mongomock
import pytest

from spider_executor.service import MongoControlService

COMMIT_SHA = "a" * 40


def test_succeeded_doctor_task_handoff_updates_revision_and_schedules_execution() -> None:
    provisioned = []
    service = MongoControlService(
        mongomock.MongoClient().spider,
        release_provider=lambda: "b" * 40,
        provisioner=provisioned.append,
    )
    service.ensure_indexes()
    registration = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {
            "$set": {
                "status": "succeeded",
                "result": {
                    "commit_sha": COMMIT_SHA,
                    "metadata": {
                        "website": "https://example.com/contact",
                        "extracted_fields": ["NAME", "DESCRIPTION"],
                        "null_fields": ["EMAIL", "OPENING_HOURS"],
                    },
                },
            }
        },
    )

    first = service.consume_doctor_handoff(registration["task_id"])
    second = service.consume_doctor_handoff(registration["task_id"])

    assert first is not None
    assert second is not None
    assert first.id == second.id
    assert first.entry_id == "business-123"
    assert first.scraper_release == COMMIT_SHA
    assert provisioned == [COMMIT_SHA]
    entry = service.get_entry("business-123")
    assert entry is not None
    assert entry.scraper_release == COMMIT_SHA
    assert entry.website == "https://example.com/contact"
    assert entry.validation.required_fields == ["NAME", "DESCRIPTION"]
    assert entry.validation.allowed_null_fields == ["EMAIL", "OPENING_HOURS"]
    assert entry.validation.minimum_non_null_fields == 2
    assert entry.validation.allowed_source_hosts == ["example.com"]
    task = service.db.doctor_tasks.find_one({"_id": registration["task_id"]})
    assert task["handoff_job_id"] == first.id
    assert service.db.execution_jobs.count_documents({"entry_id": "business-123"}) == 1


def test_provisioning_side_effect_runs_outside_mongo_transaction() -> None:
    from contextlib import contextmanager

    in_transaction = False

    @contextmanager
    def tracked_transaction():
        nonlocal in_transaction
        in_transaction = True
        try:
            yield None
        finally:
            in_transaction = False

    def provision(_release: str) -> None:
        assert not in_transaction

    service = MongoControlService(
        mongomock.MongoClient().spider,
        release_provider=lambda: "b" * 40,
        provisioner=provision,
    )
    service._transaction = tracked_transaction
    registration = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": COMMIT_SHA}}},
    )

    assert service.consume_doctor_handoff(registration["task_id"]) is not None


def test_handoff_fails_closed_when_another_entry_is_already_activated() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    first = service.register("business-1", "First AG", "Bern")
    second = service.register("business-2", "Second AG", "Zurich")
    service.db.doctor_tasks.update_one(
        {"_id": first["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": "a" * 40}}},
    )
    service.db.doctor_tasks.update_one(
        {"_id": second["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": "c" * 40}}},
    )
    service.consume_doctor_handoff(first["task_id"])

    with pytest.raises(RuntimeError, match="only one activated entry"):
        service.consume_doctor_handoff(second["task_id"])

    assert service.get_entry("business-2").scraper_release is None
    assert service.db.execution_jobs.count_documents({"entry_id": "business-2"}) == 0


def test_doctor_handoff_requires_succeeded_task_with_exact_commit_sha() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    registration = service.register("business-123", "Example AG", "Bern")

    assert service.consume_doctor_handoff(registration["task_id"]) is None
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": "not-a-sha"}}},
    )
    assert service.consume_doctor_handoff(registration["task_id"]) is None
    assert service.db.execution_jobs.count_documents({}) == 0


def test_next_handoff_discovers_persisted_succeeded_task() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    registration = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": COMMIT_SHA}}},
    )

    job = service.consume_next_doctor_handoff()

    assert job is not None
    assert job.entry_id == "business-123"
    assert job.scraper_release == COMMIT_SHA
