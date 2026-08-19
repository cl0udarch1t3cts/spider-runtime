import mongomock

from spider_executor.models import (
    Artifact,
    Entry,
    ExecutionJob,
    ExecutionRun,
    JobStatus,
    ScrapedRecord,
)
from spider_executor.service import MongoControlService


def test_success_completion_is_fenced_and_idempotent() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.ensure_indexes()
    service.put_entry(
        Entry(entry_id="example", businessname="Example", address="Bern", scraper_release="a" * 40)
    )
    service.db.runtime_state.insert_one(
        {"_id": "activated_entry", "entry_id": "example", "scraper_release": "a" * 40}
    )
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="complete"))
    claimed = service.claim("worker-1")
    run = ExecutionRun(
        id=f"{claimed.id}:{claimed.attempts}",
        job_id=claimed.id,
        entry_id="example",
        status=JobStatus.RUNNING,
    )
    record = ScrapedRecord(
        entry_id="example",
        website="https://example.com",
        fields={"NAME": {"value": "Example", "source": "https://example.com"}},
    )
    artifact = Artifact(key=f"runs/{run.id}/output.json", size_bytes=1, sha256="0" * 64)

    assert service.complete_success(claimed, run, record, artifact)
    assert not service.complete_success(claimed, run, record, artifact)
    assert service.db.records.count_documents({}) == 1
    assert service.db.execution_runs.count_documents({}) == 1
    assert service.db.artifacts.count_documents({}) == 1
    assert service.get_job(claimed.id).status == JobStatus.SUCCEEDED


def test_stale_completion_writes_no_record() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.ensure_indexes()
    service.put_entry(
        Entry(entry_id="example", businessname="Example", address="Bern", scraper_release="a" * 40)
    )
    service.db.runtime_state.insert_one(
        {"_id": "activated_entry", "entry_id": "example", "scraper_release": "a" * 40}
    )
    service.enqueue(ExecutionJob(entry_id="example", idempotency_key="stale"))
    stale = service.claim("worker-1")
    service.jobs.collection.update_one(
        {"_id": stale.id},
        {"$set": {"lease.token": "replacement-token"}},
    )
    run = ExecutionRun(
        id=f"{stale.id}:{stale.attempts}",
        job_id=stale.id,
        entry_id="example",
        status=JobStatus.RUNNING,
    )
    record = ScrapedRecord(entry_id="example", fields={})
    artifact = Artifact(key=f"runs/{run.id}/output.json", size_bytes=1, sha256="0" * 64)

    assert not service.complete_success(stale, run, record, artifact)
    assert service.db.records.count_documents({}) == 0
    assert service.db.artifacts.count_documents({}) == 0
