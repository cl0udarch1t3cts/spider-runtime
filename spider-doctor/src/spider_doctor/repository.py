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
        indexes = self.collection.index_information()
        for legacy_name in ("active_repair_per_slug", "active_task_per_entry"):
            if legacy_name in indexes:
                self.collection.drop_index(legacy_name)
        self.collection.create_index(
            "active_key", name="active_doctor_task_per_entry", unique=True, sparse=True
        )

    @property
    def _eligible(self) -> dict:
        return {
            "$or": [
                {"type": "create"},
                {"type": "repair", "failure_class": {"$in": list(self._ELIGIBLE_FAILURES)}},
            ]
        }

    def claim(
        self,
        worker_id: str,
        *,
        now: datetime | None = None,
        lease_for: timedelta = timedelta(minutes=30),
    ) -> DoctorTask | None:
        now = now or datetime.now(UTC)
        eligible = self._eligible
        # A commit already recorded in result is durable proof that publication
        # completed. Reconcile stale queued/running state before considering any
        # work so a published candidate can never be replayed indefinitely.
        self.collection.update_many(
            {
                "status": {
                    "$in": [str(DoctorStatus.QUEUED), str(DoctorStatus.RUNNING)]
                },
                "candidate_sha": {"$type": "string"},
                "result.commit_sha": {"$type": "string"},
                "$expr": {"$eq": ["$candidate_sha", "$result.commit_sha"]},
                **eligible,
            },
            {
                "$set": {
                    "status": str(DoctorStatus.SUCCEEDED),
                    "lease": None,
                    "updated_at": now,
                },
                "$unset": {"active_key": ""},
            },
        )
        self.collection.update_many(
            {
                "status": str(DoctorStatus.RUNNING),
                "lease.expires_at": {"$lte": now},
                "candidate_sha": {"$exists": False},
                "$expr": {"$gte": ["$attempts", "$max_attempts"]},
                **eligible,
            },
            {
                "$set": {
                    "status": str(DoctorStatus.EXHAUSTED),
                    "lease": None,
                    "updated_at": now,
                },
                "$unset": {"active_key": ""},
            },
        )

        # A crash after candidate persistence must be reconcilable even when the
        # generation attempt consumed the retry budget. This reclaim does not
        # consume another generation attempt.
        token = str(uuid4())
        candidate = self.collection.find_one_and_update(
            {
                "$and": [
                    {"candidate_sha": {"$type": "string"}},
                    {
                        "$or": [
                            {
                                "status": str(DoctorStatus.QUEUED),
                                "available_at": {"$lte": now},
                            },
                            {
                                "status": str(DoctorStatus.RUNNING),
                                "lease.expires_at": {"$lte": now},
                            },
                        ]
                    },
                    eligible,
                ],
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
                }
            },
            sort=[("priority", DESCENDING), ("created_at", ASCENDING)],
            return_document=ReturnDocument.AFTER,
        )
        if candidate:
            return DoctorTask.model_validate(candidate)

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

    def release(
        self,
        task_id: str,
        lease_token: str,
        *,
        now: datetime | None = None,
        retry_after: timedelta = timedelta(minutes=30),
    ) -> bool:
        """Return a claimed generation task to the queue without consuming
        the attempt claim() charged for it. Deferrals (e.g. the subscription
        budget gate) are not failures and must not eat the retry budget."""
        now = now or datetime.now(UTC)
        outcome = self.collection.update_one(
            {
                "_id": task_id,
                "status": str(DoctorStatus.RUNNING),
                "lease.token": lease_token,
                "lease.expires_at": {"$gt": now},
                "candidate_sha": {"$exists": False},
            },
            {
                "$set": {
                    "status": str(DoctorStatus.QUEUED),
                    "lease": None,
                    "available_at": now + retry_after,
                    "updated_at": now,
                },
                "$inc": {"attempts": -1},
            },
        )
        return outcome.modified_count == 1

    def record_model(
        self,
        task_id: str,
        lease_token: str,
        model: str,
        *,
        now: datetime | None = None,
    ) -> bool:
        """Stamp the model chosen for the current attempt (ADR-008 audit)."""
        outcome = self.collection.update_one(
            {"_id": task_id, "lease.token": lease_token},
            {"$set": {"model": model, "updated_at": now or datetime.now(UTC)}},
        )
        return outcome.modified_count == 1

    def record_candidate(
        self,
        task_id: str,
        lease_token: str,
        candidate_sha: str,
        result: dict,
        *,
        now: datetime | None = None,
    ) -> bool:
        if not re.fullmatch(r"[0-9a-f]{40}", candidate_sha):
            raise ValueError("candidate SHA must be a full Git SHA")
        now = now or datetime.now(UTC)
        # A valid lease may replace an earlier candidate_sha: publication rebases
        # a stale candidate onto the moved branch tip, which produces a new SHA
        # for the same validated patch.
        outcome = self.collection.update_one(
            {
                "_id": task_id,
                "status": str(DoctorStatus.RUNNING),
                "lease.token": lease_token,
                "lease.expires_at": {"$gt": now},
            },
            {
                "$set": {
                    "candidate_sha": candidate_sha,
                    "candidate_result": result,
                    "updated_at": now,
                }
            },
        )
        return outcome.modified_count == 1 or (
            outcome.matched_count == 1
            and self.collection.find_one({"_id": task_id}, {"candidate_sha": 1}).get("candidate_sha")
            == candidate_sha
        )

    def complete_publication(
        self,
        task_id: str,
        lease_token: str,
        candidate_sha: str,
        *,
        now: datetime | None = None,
    ) -> bool:
        now = now or datetime.now(UTC)
        document = self.collection.find_one(
            {
                "_id": task_id,
                "status": str(DoctorStatus.RUNNING),
                "lease.token": lease_token,
                "lease.expires_at": {"$gt": now},
                "candidate_sha": candidate_sha,
            },
            {"candidate_result": 1},
        )
        if document is None or not isinstance(document.get("candidate_result"), dict):
            return False
        result = {**document["candidate_result"], "commit_sha": candidate_sha}
        outcome = self.collection.update_one(
            {
                "_id": task_id,
                "status": str(DoctorStatus.RUNNING),
                "lease.token": lease_token,
                "lease.expires_at": {"$gt": now},
                "candidate_sha": candidate_sha,
            },
            {
                "$set": {
                    "status": str(DoctorStatus.SUCCEEDED),
                    "result": result,
                    "lease": None,
                    "updated_at": now,
                },
                "$unset": {"active_key": ""},
            },
        )
        return outcome.modified_count == 1

    def resolve_no_website(
        self,
        task_id: str,
        lease_token: str,
        summary: str,
        *,
        now: datetime | None = None,
    ) -> bool:
        """Terminal, fenced resolution: no trustworthy website exists.

        A finding rather than a failure — no retry budget is consumed,
        last_error stays empty, and the task becomes unclaimable.
        """
        now = now or datetime.now(UTC)
        outcome = self.collection.update_one(
            {
                "_id": task_id,
                "status": str(DoctorStatus.RUNNING),
                "lease.token": lease_token,
                "lease.expires_at": {"$gt": now},
            },
            {
                "$set": {
                    "status": str(DoctorStatus.NO_WEBSITE),
                    "lease": None,
                    "result": {
                        "resolution": "no_reliable_website",
                        "summary": summary[:2000],
                    },
                    "updated_at": now,
                },
                "$unset": {"active_key": ""},
            },
        )
        return outcome.modified_count == 1

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
        current = self.collection.find_one(
            {
                "_id": task_id,
                "status": str(DoctorStatus.RUNNING),
                "lease.token": lease_token,
                "lease.expires_at": {"$gt": now},
            },
            {"candidate_sha": 1},
        )
        if current is None:
            return None
        has_candidate = isinstance(current.get("candidate_sha"), str)
        status = (
            DoctorStatus.QUEUED
            if has_candidate or attempts < max_attempts
            else DoctorStatus.EXHAUSTED
        )
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
