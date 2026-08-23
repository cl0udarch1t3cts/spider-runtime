"""Real-MongoDB smoke test executed inside the isolated control network."""

import os

from pymongo import MongoClient

from spider_executor.models import (
    Artifact,
    Entry,
    ExecutionJob,
    ExecutionRun,
    JobStatus,
    ScrapedRecord,
)
from spider_executor.service import MongoControlService


def main() -> None:
    client = MongoClient(os.environ["SPIDER_TEST_MONGODB_URI"], serverSelectionTimeoutMS=5000)
    db = client.get_database("spider_integration")
    client.drop_database(db.name)
    service = MongoControlService(db)
    service.ensure_indexes()

    service.put_entry(
        Entry(
            entry_id="example",
            businessname="First",
            address="Bern",
            website="https://example.com",
            scraper_release="a" * 40,
        )
    )
    updated = service.put_entry(
        Entry(
            entry_id="example",
            businessname="Updated",
            address="Bern",
            website="https://example.com",
            scraper_release="a" * 40,
        )
    )
    assert updated.businessname == "Updated"

    # enqueue() only accepts the activated entry/release pair; mirror the
    # activation record that consume_doctor_handoff() writes.
    db.runtime_state.replace_one(
        {"_id": "activated_entry"},
        {"_id": "activated_entry", "entry_id": "example", "scraper_release": "a" * 40},
        upsert=True,
    )

    job = service.enqueue(ExecutionJob(entry_id="example", idempotency_key="integration:1"))
    assert service.enqueue(ExecutionJob(entry_id="example", idempotency_key="integration:1")).id == job.id
    claimed = service.claim("integration-worker")
    assert claimed is not None and claimed.lease is not None

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
    artifact = Artifact(
        key=f"runs/{run.id}/output.json",
        size_bytes=1,
        sha256="0" * 64,
    )
    assert service.complete_success(claimed, run, record, artifact)
    assert service.get_job(claimed.id).status == JobStatus.SUCCEEDED
    assert service.get_record(run.id).fields["NAME"].value == "Example"
    client.drop_database(db.name)
    print("real MongoDB transaction smoke test passed")


if __name__ == "__main__":
    main()
