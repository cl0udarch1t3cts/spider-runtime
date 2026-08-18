from datetime import UTC, datetime, timedelta

import mongomock

from spider_doctor.models import DoctorStatus
from spider_doctor.repository import MongoDoctorTaskRepository


def queued_task(task_id: str, *, priority: int = 50, max_attempts: int = 2) -> dict:
    now = datetime.now(UTC)
    return {
        "_id": task_id,
        "active_key": "example",
        "slug": "example",
        "type": "repair",
        "status": "queued",
        "priority": priority,
        "attempts": 0,
        "max_attempts": max_attempts,
        "available_at": now - timedelta(seconds=1),
        "source_run_id": "job:1",
        "failure_class": "SCRAPER_EXCEPTION",
        "errors": ["traceback"],
        "created_at": now,
        "updated_at": now,
    }


def test_claim_is_atomic_prioritized_and_leased() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_many([queued_task("low", priority=10), queued_task("high", priority=90)])
    repo = MongoDoctorTaskRepository(collection)

    claimed = repo.claim("doctor-1", lease_for=timedelta(minutes=2))

    assert claimed is not None
    assert claimed.id == "high"
    assert claimed.status == DoctorStatus.RUNNING
    assert claimed.attempts == 1
    assert claimed.lease is not None
    assert claimed.lease.worker_id == "doctor-1"


def test_ensure_indexes_backfills_legacy_executor_tasks() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(
        {
            "_id": "legacy",
            "active_key": "example",
            "slug": "example",
            "type": "repair",
            "status": "queued",
            "source_run_id": "job:1",
            "failure_class": "SCRAPER_EXCEPTION",
        }
    )
    repo = MongoDoctorTaskRepository(collection)

    repo.ensure_indexes()
    claimed = repo.claim("doctor-1")

    assert claimed is not None
    assert claimed.id == "legacy"
    assert claimed.attempts == 1
    assert claimed.max_attempts == 2


def test_stale_lease_cannot_complete_task() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("task"))
    repo = MongoDoctorTaskRepository(collection)
    stale = repo.claim("doctor-1", lease_for=timedelta(seconds=1))
    collection.update_one({"_id": stale.id}, {"$set": {"lease.token": "replacement"}})

    assert not repo.complete(stale.id, stale.lease.token, DoctorStatus.AWAITING_REVIEW, {"summary": "fixed"})
    assert collection.find_one({"_id": stale.id})["status"] == "running"


def test_expired_lease_cannot_complete_even_before_reclaim() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("expired"))
    repo = MongoDoctorTaskRepository(collection)
    now = datetime.now(UTC)
    claimed = repo.claim("doctor-1", now=now, lease_for=timedelta(seconds=1))

    assert not repo.complete(
        claimed.id,
        claimed.lease.token,
        DoctorStatus.AWAITING_REVIEW,
        {"summary": "late"},
        now=now + timedelta(seconds=2),
    )
    assert collection.find_one({"_id": claimed.id})["status"] == "running"


def test_claim_ignores_noneligible_operational_failure() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    document = queued_task("network")
    document["failure_class"] = "NETWORK_TIMEOUT"
    collection.insert_one(document)
    repo = MongoDoctorTaskRepository(collection)

    assert repo.claim("doctor-1") is None
    assert collection.find_one({"_id": "network"})["status"] == "queued"


def test_expired_final_attempt_becomes_exhausted() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("task", max_attempts=1))
    repo = MongoDoctorTaskRepository(collection)
    now = datetime.now(UTC)
    claimed = repo.claim("doctor-1", now=now, lease_for=timedelta(seconds=1))

    assert repo.claim("doctor-2", now=now + timedelta(seconds=2)) is None
    exhausted = collection.find_one({"_id": claimed.id})
    assert exhausted["status"] == "exhausted"
    assert "active_key" not in exhausted


def test_failed_attempt_is_requeued_with_backoff_until_exhausted() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("task", max_attempts=2))
    repo = MongoDoctorTaskRepository(collection)
    now = datetime.now(UTC)
    claimed = repo.claim("doctor-1", now=now)

    status = repo.fail_attempt(
        claimed.id,
        claimed.lease.token,
        "agent failed",
        attempts=claimed.attempts,
        max_attempts=claimed.max_attempts,
        now=now,
        retry_after=timedelta(minutes=5),
    )

    document = collection.find_one({"_id": claimed.id})
    assert status == DoctorStatus.QUEUED
    assert document["status"] == "queued"
    actual_available = document["available_at"].replace(tzinfo=UTC)
    assert abs((actual_available - (now + timedelta(minutes=5))).total_seconds()) < 0.001
    assert document["last_error"] == "agent failed"


def test_enqueue_create_task_is_idempotent_and_pins_base_release() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    repo = MongoDoctorTaskRepository(collection)

    first = repo.enqueue_create(
        slug="new-place",
        name="New Place",
        address="Main Street 1, 8000 Zürich",
        base_release="a" * 40,
    )
    second = repo.enqueue_create(
        slug="new-place",
        name="New Place",
        address="Main Street 1, 8000 Zürich",
        base_release="a" * 40,
    )

    assert first.id == second.id
    assert collection.count_documents({}) == 1
    assert first.type == "create"
    assert first.scraper_release == "a" * 40
    assert first.request["address"] == "Main Street 1, 8000 Zürich"
