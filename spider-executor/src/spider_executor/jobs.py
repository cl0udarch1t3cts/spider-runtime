from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from pymongo import ASCENDING, DESCENDING, ReturnDocument
from pymongo.collection import Collection

from spider_executor.models import ExecutionJob, JobStatus


def _doc(job: ExecutionJob) -> dict:
    data = job.model_dump(mode="python")
    data["_id"] = data.pop("id")
    data["status"] = str(job.status)
    return data


def _job(document: dict | None) -> ExecutionJob | None:
    if document is None:
        return None
    data = dict(document)
    data["id"] = str(data.pop("_id"))
    return ExecutionJob.model_validate(data)


class MongoJobRepository:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def ensure_indexes(self) -> None:
        self.collection.create_index("idempotency_key", unique=True)
        self.collection.create_index(
            [("status", ASCENDING), ("available_at", ASCENDING), ("priority", DESCENDING), ("created_at", ASCENDING)]
        )
        self.collection.create_index("lease.expires_at")

    def enqueue(self, job: ExecutionJob) -> ExecutionJob:
        self.collection.update_one(
            {"idempotency_key": job.idempotency_key},
            {"$setOnInsert": _doc(job)},
            upsert=True,
        )
        return _job(self.collection.find_one({"idempotency_key": job.idempotency_key}))

    def claim(
        self,
        worker_id: str,
        *,
        now: datetime | None = None,
        lease_for: timedelta = timedelta(minutes=5),
    ) -> ExecutionJob | None:
        now = now or datetime.now(UTC)
        self.collection.update_many(
            {
                "status": str(JobStatus.RUNNING),
                "lease.expires_at": {"$lte": now},
                "$expr": {"$gte": ["$attempts", "$max_attempts"]},
            },
            {
                "$set": {
                    "status": str(JobStatus.EXHAUSTED),
                    "lease": None,
                    "updated_at": now,
                }
            },
        )
        lease_token = str(uuid4())
        document = self.collection.find_one_and_update(
            {
                "$or": [
                    {"status": str(JobStatus.QUEUED), "available_at": {"$lte": now}},
                    {"status": str(JobStatus.RUNNING), "lease.expires_at": {"$lte": now}},
                ],
                "$expr": {"$lt": ["$attempts", "$max_attempts"]},
            },
            {
                "$set": {
                    "status": str(JobStatus.RUNNING),
                    "lease": {
                        "worker_id": worker_id,
                        "token": lease_token,
                        "expires_at": now + lease_for,
                    },
                    "updated_at": now,
                },
                "$inc": {"attempts": 1},
            },
            sort=[("priority", DESCENDING), ("created_at", ASCENDING)],
            return_document=ReturnDocument.AFTER,
        )
        return _job(document)

    def get(self, job_id: str) -> ExecutionJob | None:
        return _job(self.collection.find_one({"_id": job_id}))

    def count(self) -> int:
        return self.collection.count_documents({})

    def finish(
        self,
        job_id: str,
        lease_token: str,
        status: JobStatus,
        *,
        now: datetime | None = None,
    ) -> bool:
        result = self.collection.update_one(
            {
                "_id": job_id,
                "status": str(JobStatus.RUNNING),
                "lease.token": lease_token,
            },
            {"$set": {"status": str(status), "lease": None, "updated_at": now or datetime.now(UTC)}},
        )
        return result.modified_count == 1
