from datetime import UTC, datetime, timedelta

import mongomock

from spider_executor.jobs import MongoJobRepository
from spider_executor.models import ExecutionJob, JobStatus


def test_idempotency_key_prevents_duplicate_jobs() -> None:
    repo = MongoJobRepository(mongomock.MongoClient().db.execution_jobs)
    job = ExecutionJob(slug="example", idempotency_key="manual:example:1")
    first = repo.enqueue(job)
    second = repo.enqueue(job)
    assert first.id == second.id
    assert repo.count() == 1


def test_worker_atomically_claims_highest_priority_available_job() -> None:
    repo = MongoJobRepository(mongomock.MongoClient().db.execution_jobs)
    now = datetime.now(UTC)
    available = now - timedelta(seconds=1)
    repo.enqueue(ExecutionJob(slug="low", idempotency_key="low", priority=10, available_at=available))
    repo.enqueue(ExecutionJob(slug="high", idempotency_key="high", priority=90, available_at=available))

    claimed = repo.claim("worker-1", now=now, lease_for=timedelta(minutes=5))

    assert claimed is not None
    assert claimed.slug == "high"
    assert claimed.status == JobStatus.RUNNING
    assert claimed.lease.worker_id == "worker-1"


def test_stale_worker_cannot_finish_reclaimed_job() -> None:
    repo = MongoJobRepository(mongomock.MongoClient().db.execution_jobs)
    now = datetime.now(UTC)
    repo.enqueue(
        ExecutionJob(
            slug="example",
            idempotency_key="fenced",
            available_at=now - timedelta(seconds=1),
        )
    )
    stale = repo.claim("worker-1", now=now, lease_for=timedelta(seconds=1))
    current = repo.claim(
        "worker-2", now=now + timedelta(seconds=2), lease_for=timedelta(minutes=5)
    )

    assert stale.lease.token != current.lease.token
    assert not repo.finish(stale.id, stale.lease.token, JobStatus.SUCCEEDED)
    assert repo.finish(current.id, current.lease.token, JobStatus.SUCCEEDED)
    assert repo.get(current.id).status == JobStatus.SUCCEEDED


def test_expired_final_attempt_becomes_exhausted() -> None:
    repo = MongoJobRepository(mongomock.MongoClient().db.execution_jobs)
    now = datetime.now(UTC)
    repo.enqueue(
        ExecutionJob(
            slug="example",
            idempotency_key="exhausted",
            max_attempts=1,
            available_at=now - timedelta(seconds=1),
        )
    )
    claimed = repo.claim("worker-1", now=now, lease_for=timedelta(seconds=1))

    assert repo.claim("worker-2", now=now + timedelta(seconds=2)) is None
    assert repo.get(claimed.id).status == JobStatus.EXHAUSTED


def test_expired_lease_can_be_reclaimed() -> None:
    repo = MongoJobRepository(mongomock.MongoClient().db.execution_jobs)
    now = datetime.now(UTC)
    enqueued = repo.enqueue(ExecutionJob(slug="example", idempotency_key="lease"))
    first = repo.claim("dead-worker", now=now, lease_for=timedelta(seconds=1))
    assert first is not None

    reclaimed = repo.claim("new-worker", now=now + timedelta(seconds=2), lease_for=timedelta(minutes=5))
    assert reclaimed is not None
    assert reclaimed.id == enqueued.id
    assert reclaimed.lease.worker_id == "new-worker"
