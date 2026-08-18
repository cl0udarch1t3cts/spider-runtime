from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from pymongo import ASCENDING, DESCENDING, ReturnDocument
from pymongo.collection import Collection

from spider_doctor.models import DoctorStatus, DoctorTask


class MongoDoctorTaskRepository:
    _ELIGIBLE_FAILURES = (
        "SCRAPER_EXCEPTION",
        "OUTPUT_SCHEMA_FAILURE",
        "SEMANTIC_VALIDATION_FAILURE",
        "IDENTITY_MISMATCH",
    )

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def ensure_indexes(self) -> None:
        now = datetime.now(UTC)
        defaults = {
            "priority": 50,
            "attempts": 0,
            "max_attempts": 2,
            "available_at": now,
            "lease": None,
            "errors": [],
            "created_at": now,
            "updated_at": now,
        }
        for field, value in defaults.items():
            self.collection.update_many({field: {"$exists": False}}, {"$set": {field: value}})
        self.collection.create_index(
            [("status", ASCENDING), ("available_at", ASCENDING), ("priority", DESCENDING)]
        )
        self.collection.create_index("lease.expires_at")
        self.collection.create_index(
            "active_key",
            name="active_repair_per_slug",
            unique=True,
            sparse=True,
        )

    def enqueue_create(
        self,
        *,
        slug: str,
        name: str,
        address: str,
        base_release: str,
        website: str | None = None,
        priority: int = 40,
    ) -> DoctorTask:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,127}", slug):
            raise ValueError("invalid scraper slug")
        if not name.strip() or not address.strip():
            raise ValueError("new scraper tasks require a name and address")
        if not re.fullmatch(r"[0-9a-f]{40}", base_release):
            raise ValueError("base release must be a full Git SHA")
        now = datetime.now(UTC)
        request = {"name": name.strip(), "address": address.strip()}
        if website:
            request["website"] = website.strip()
        self.collection.update_one(
            {"active_key": slug},
            {
                "$setOnInsert": {
                    "_id": str(uuid4()),
                    "active_key": slug,
                    "slug": slug,
                    "type": "create",
                    "status": str(DoctorStatus.QUEUED),
                    "priority": priority,
                    "attempts": 0,
                    "max_attempts": 2,
                    "available_at": now,
                    "source_run_id": None,
                    "failure_class": "NEW_SCRAPER",
                    "errors": [],
                    "scraper_release": base_release,
                    "request": request,
                    "lease": None,
                    "created_at": now,
                    "updated_at": now,
                }
            },
            upsert=True,
        )
        document = self.collection.find_one({"active_key": slug})
        task = DoctorTask.model_validate(document)
        if task.type != "create" or task.request != request or task.scraper_release != base_release:
            raise ValueError(f"slug {slug!r} already has a different active Doctor task")
        return task

    def claim(
        self,
        worker_id: str,
        *,
        now: datetime | None = None,
        lease_for: timedelta = timedelta(minutes=30),
    ) -> DoctorTask | None:
        now = now or datetime.now(UTC)
        eligible = {
            "$or": [
                {"type": "create"},
                {"type": "repair", "failure_class": {"$in": list(self._ELIGIBLE_FAILURES)}},
            ]
        }
        self.collection.update_many(
            {
                "status": str(DoctorStatus.RUNNING),
                "lease.expires_at": {"$lte": now},
                "$expr": {"$gte": ["$attempts", "$max_attempts"]},
                **eligible,
            },
            {
                "$set": {
                    "status": str(DoctorStatus.EXHAUSTED),
                    "lease": None,
                    "updated_at": now,
                }
            },
        )
        token = str(uuid4())
        document = self.collection.find_one_and_update(
            {
                "$and": [
                    {
                        "$or": [
                            {"status": str(DoctorStatus.QUEUED), "available_at": {"$lte": now}},
                            {
                                "status": str(DoctorStatus.RUNNING),
                                "lease.expires_at": {"$lte": now},
                            },
                        ]
                    },
                    eligible,
                ],
                "$expr": {"$lt": ["$attempts", "$max_attempts"]},
            },
            {
                "$set": {
                    "status": str(DoctorStatus.RUNNING),
                    "lease": {
                        "worker_id": worker_id,
                        "token": token,
                        "expires_at": now + lease_for,
                    },
                    "updated_at": now,
                },
                "$inc": {"attempts": 1},
            },
            sort=[("priority", DESCENDING), ("created_at", ASCENDING)],
            return_document=ReturnDocument.AFTER,
        )
        return DoctorTask.model_validate(document) if document else None

    def fail_attempt(
        self,
        task_id: str,
        lease_token: str,
        error: str,
        *,
        attempts: int,
        max_attempts: int,
        now: datetime | None = None,
        retry_after: timedelta = timedelta(minutes=5),
    ) -> DoctorStatus | None:
        now = now or datetime.now(UTC)
        status = DoctorStatus.EXHAUSTED if attempts >= max_attempts else DoctorStatus.QUEUED
        set_values = {
            "status": str(status),
            "last_error": error[:4000],
            "lease": None,
            "updated_at": now,
        }
        if status == DoctorStatus.QUEUED:
            set_values["available_at"] = now + retry_after
        update: dict = {"$set": set_values}
        if status == DoctorStatus.EXHAUSTED:
            update["$unset"] = {"active_key": ""}
        outcome = self.collection.update_one(
            {
                "_id": task_id,
                "status": str(DoctorStatus.RUNNING),
                "lease.token": lease_token,
                "lease.expires_at": {"$gt": now},
            },
            update,
        )
        return status if outcome.modified_count == 1 else None

    def complete(
        self,
        task_id: str,
        lease_token: str,
        status: DoctorStatus,
        result: dict,
        *,
        now: datetime | None = None,
    ) -> bool:
        if status != DoctorStatus.AWAITING_REVIEW:
            raise ValueError("only reviewable patches may complete a Doctor task")
        now = now or datetime.now(UTC)
        update = {
            "$set": {
                "status": str(status),
                "result": result,
                "lease": None,
                "updated_at": now or datetime.now(UTC),
            }
        }
        outcome = self.collection.update_one(
            {
                "_id": task_id,
                "status": str(DoctorStatus.RUNNING),
                "lease.token": lease_token,
                "lease.expires_at": {"$gt": now},
            },
            update,
        )
        return outcome.modified_count == 1
