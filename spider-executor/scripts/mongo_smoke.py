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

    service.put_entry(Entry(slug="example", name="First", website="https://example.com"))
    updated = service.put_entry(Entry(slug="example", name="Updated", website="https://example.com"))
    assert updated.name == "Updated"

    job = service.enqueue(ExecutionJob(slug="example", idempotency_key="integration:1"))
    assert service.enqueue(ExecutionJob(slug="example", idempotency_key="integration:1")).id == job.id
    claimed = service.claim("integration-worker")
    assert claimed is not None and claimed.lease is not None

    run = ExecutionRun(
        id=f"{claimed.id}:{claimed.attempts}",
        job_id=claimed.id,
        slug="example",
        status=JobStatus.RUNNING,
    )
    record = ScrapedRecord(
        slug="example",
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
