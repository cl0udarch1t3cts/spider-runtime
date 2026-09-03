from datetime import UTC, datetime, timedelta

import mongomock

from spider_doctor.models import DoctorStatus
from spider_doctor.repository import MongoDoctorTaskRepository


def queued_task(task_id: str, *, priority: int = 50, max_attempts: int = 2) -> dict:
    now = datetime.now(UTC)
    return {
        "_id": task_id,
        "active_key": "Entry_1",
        "entry_id": "Entry_1",
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
    assert claimed.entry_id == "Entry_1"
    assert claimed.status == DoctorStatus.RUNNING
    assert claimed.attempts == 1
    assert claimed.lease is not None


def test_ensure_indexes_backfills_executor_tasks_without_slug() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(
        {
            "_id": "legacy",
            "active_key": "Entry_1",
            "entry_id": "Entry_1",
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
    assert claimed.attempts == 1
    assert claimed.max_attempts == 2


def test_stale_or_expired_lease_cannot_persist_candidate() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("task"))
    repo = MongoDoctorTaskRepository(collection)
    now = datetime.now(UTC)
    claimed = repo.claim("doctor-1", now=now, lease_for=timedelta(seconds=1))

    assert not repo.record_candidate(
        claimed.id,
        claimed.lease.token,
        "a" * 40,
        {"summary": "verified"},
        now=now + timedelta(seconds=2),
    )
    assert "candidate_sha" not in collection.find_one({"_id": claimed.id})


def test_candidate_is_durable_before_publication_and_completion_is_fenced() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("task"))
    repo = MongoDoctorTaskRepository(collection)
    claimed = repo.claim("doctor-1")
    result = {"summary": "verified", "changed_files": ["scrapers/Entry_1/scrape.py"]}

    assert repo.record_candidate(claimed.id, claimed.lease.token, "a" * 40, result)
    durable = collection.find_one({"_id": claimed.id})
    assert durable["candidate_sha"] == "a" * 40
    assert durable["candidate_result"] == result
    assert not repo.complete_publication(claimed.id, "wrong", "a" * 40)
    assert repo.complete_publication(claimed.id, claimed.lease.token, "a" * 40)
    completed = collection.find_one({"_id": claimed.id})
    assert completed["status"] == "succeeded"
    assert completed["result"]["commit_sha"] == "a" * 40
    assert completed["lease"] is None
    assert "active_key" not in completed


def test_valid_lease_can_replace_candidate_with_rebased_sha() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("task"))
    repo = MongoDoctorTaskRepository(collection)
    claimed = repo.claim("doctor-1")
    result = {"summary": "verified"}

    assert repo.record_candidate(claimed.id, claimed.lease.token, "a" * 40, result)
    assert repo.record_candidate(claimed.id, claimed.lease.token, "b" * 40, result)
    assert collection.find_one({"_id": claimed.id})["candidate_sha"] == "b" * 40
    assert repo.complete_publication(claimed.id, claimed.lease.token, "b" * 40)


def test_claim_reconciles_already_published_candidate_without_reprocessing() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    document = queued_task("published")
    document.update(
        {
            "status": "running",
            "attempts": 1,
            "candidate_sha": "a" * 40,
            "candidate_result": {"status": "awaiting_review", "summary": "verified"},
            "result": {"status": "awaiting_review", "commit_sha": "a" * 40},
            "lease": {
                "worker_id": "doctor-old",
                "token": "old-token",
                "expires_at": datetime.now(UTC) + timedelta(minutes=30),
            },
        }
    )
    collection.insert_one(document)
    repo = MongoDoctorTaskRepository(collection)

    assert repo.claim("doctor-new") is None

    reconciled = collection.find_one({"_id": "published"})
    assert reconciled is not None
    assert reconciled["status"] == "succeeded"
    assert reconciled["lease"] is None
    assert "active_key" not in reconciled


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


def test_persisted_candidate_is_requeued_for_publication_without_new_attempt() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("task", max_attempts=1))
    repo = MongoDoctorTaskRepository(collection)
    now = datetime.now(UTC)
    claimed = repo.claim("doctor-1", now=now)
    assert repo.record_candidate(
        claimed.id,
        claimed.lease.token,
        "a" * 40,
        {"status": "awaiting_review", "summary": "verified"},
        now=now,
    )

    status = repo.fail_attempt(
        claimed.id,
        claimed.lease.token,
        "push unavailable",
        attempts=claimed.attempts,
        max_attempts=claimed.max_attempts,
        now=now,
        retry_after=timedelta(seconds=1),
    )
    reclaimed = repo.claim("doctor-2", now=now + timedelta(seconds=2))

    assert status == DoctorStatus.QUEUED
    assert reclaimed is not None
    assert reclaimed.candidate_sha == "a" * 40
    assert reclaimed.attempts == 1


def test_claim_ignores_noneligible_operational_failure() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    document = queued_task("network")
    document["failure_class"] = "NETWORK_TIMEOUT"
    collection.insert_one(document)

    assert MongoDoctorTaskRepository(collection).claim("doctor-1") is None


def test_release_requeues_without_consuming_the_attempt() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("deferred"))
    repo = MongoDoctorTaskRepository(collection)
    claimed = repo.claim("doctor-1", lease_for=timedelta(minutes=5))
    assert claimed is not None and claimed.attempts == 1

    released = repo.release(
        claimed.id, claimed.lease.token, retry_after=timedelta(minutes=30)
    )

    assert released
    document = collection.find_one({"_id": "deferred"})
    assert document["status"] == "queued"
    assert document["attempts"] == 0
    assert document["lease"] is None
    available_at = document["available_at"].replace(tzinfo=UTC)
    assert available_at > datetime.now(UTC) + timedelta(minutes=20)
    assert repo.claim("doctor-1") is None


def test_release_refuses_a_lost_lease() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("deferred"))
    repo = MongoDoctorTaskRepository(collection)
    claimed = repo.claim("doctor-1", lease_for=timedelta(minutes=5))

    assert not repo.release(claimed.id, "stale-token")
    assert collection.find_one({"_id": "deferred"})["status"] == "running"


def test_resolve_no_website_is_terminal_fenced_and_unclaimable() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    collection.insert_one(queued_task("task-1"))
    repo = MongoDoctorTaskRepository(collection)
    claimed = repo.claim("doctor-1", lease_for=timedelta(minutes=5))

    resolved = repo.resolve_no_website(
        claimed.id, claimed.lease.token, "no official website could be verified"
    )

    assert resolved is True
    stored = collection.find_one({"_id": "task-1"})
    assert stored["status"] == "no_website"
    assert stored["lease"] is None
    assert stored.get("last_error") is None
    assert "active_key" not in stored
    assert stored["result"]["resolution"] == "no_reliable_website"
    # Terminal: nothing left to claim, and a stale token cannot resolve again.
    assert repo.claim("doctor-1") is None
    assert repo.resolve_no_website("task-1", "wrong-token", "x") is False


def test_record_model_stamps_the_attempt_model_under_a_valid_lease() -> None:
    collection = mongomock.MongoClient().spider.doctor_tasks
    repo = MongoDoctorTaskRepository(collection)
    collection.insert_one(queued_task("task-1"))
    task = repo.claim("doctor-1")

    assert repo.record_model(task.id, task.lease.token, "qwen3-coder:free") is True
    assert collection.find_one({"_id": "task-1"})["model"] == "qwen3-coder:free"

    # A stale lease must not overwrite the stamp.
    assert repo.record_model(task.id, "wrong-token", "gpt-5.4") is False
    assert collection.find_one({"_id": "task-1"})["model"] == "qwen3-coder:free"
