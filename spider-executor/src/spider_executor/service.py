from __future__ import annotations

import re
from collections.abc import Callable
from contextlib import contextmanager
from datetime import UTC, datetime
from urllib.parse import urlparse
from uuid import uuid4

from pymongo import ASCENDING, DESCENDING
from pymongo.database import Database
from pymongo.errors import PyMongoError

from spider_executor.jobs import MongoJobRepository
from spider_executor.models import (
    Artifact,
    Entry,
    ExecutionJob,
    ExecutionRun,
    FailureClass,
    JobStatus,
    ScrapedRecord,
)


def _encode(model, *, identifier: str | None = None) -> dict:
    document = model.model_dump(mode="python")
    if "id" in document:
        document["_id"] = document.pop("id")
    elif identifier is not None:
        document["_id"] = identifier
    return document


def _decode(model_type, document: dict | None, *, id_field: bool = False):
    if document is None:
        return None
    data = dict(document)
    if id_field:
        data["id"] = str(data.pop("_id"))
    else:
        data.pop("_id", None)
    return model_type.model_validate(data)


def _doctor_entry_contract(result: dict) -> dict:
    metadata = result.get("metadata")
    if metadata is None:
        return {}
    if not isinstance(metadata, dict):
        raise RuntimeError("Doctor result metadata must be an object")
    website = metadata.get("website")
    extracted = metadata.get("extracted_fields")
    null_fields = metadata.get("null_fields")
    parsed = urlparse(website) if isinstance(website, str) else None
    if parsed is None or parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise RuntimeError("Doctor result metadata must contain an absolute website URL")
    if not isinstance(extracted, list) or not isinstance(null_fields, list):
        raise RuntimeError("Doctor result metadata must contain extracted_fields and null_fields")
    field_name = re.compile(r"^[A-Z][A-Z0-9_]{0,127}$")
    if (
        not extracted
        or any(not isinstance(value, str) or not field_name.fullmatch(value) for value in extracted)
        or any(not isinstance(value, str) or not field_name.fullmatch(value) for value in null_fields)
        or len(extracted) != len(set(extracted))
        or len(null_fields) != len(set(null_fields))
        or set(extracted) & set(null_fields)
    ):
        raise RuntimeError("Doctor result field contract is invalid")
    return {
        "website": website,
        "validation": {
            "required_fields": extracted,
            "allowed_null_fields": null_fields,
            "minimum_non_null_fields": len(extracted),
            "allowed_source_hosts": [parsed.hostname.lower()],
        },
    }


class MongoControlService:
    def __init__(
        self,
        db: Database,
        *,
        release_provider: Callable[[], str] | None = None,
        provisioner: Callable[[str], None] | None = None,
    ) -> None:
        self.db = db
        self.jobs = MongoJobRepository(db.execution_jobs)
        self.release_provider = release_provider
        self.provisioner = provisioner

    def ensure_indexes(self) -> None:
        self.jobs.ensure_indexes()
        self.db.execution_runs.create_index([("entry_id", ASCENDING), ("started_at", DESCENDING)])
        self.db.records.create_index("run_id", unique=True)
        self.db.artifacts.create_index("run_id", unique=True)
        legacy_tasks = list(
            self.db.doctor_tasks.find(
                {"active_key": {"$exists": True}, "entry_id": {"$exists": True}, "type": {"$in": ["create", "repair"]}},
                {"_id": 1, "entry_id": 1, "type": 1, "active_key": 1},
            )
        )
        tasks_by_entry: dict[str, list[dict]] = {}
        for task in legacy_tasks:
            tasks_by_entry.setdefault(task["entry_id"], []).append(task)
        for entry_id, tasks in tasks_by_entry.items():
            tasks.sort(key=lambda task: (task.get("type") != "create", str(task["_id"])))
            winner, *conflicts = tasks
            self.db.doctor_tasks.update_one(
                {"_id": winner["_id"]},
                {"$set": {"active_key": entry_id}},
            )
            for conflict in conflicts:
                self.db.doctor_tasks.update_one(
                    {"_id": conflict["_id"]},
                    {
                        "$set": {
                            "status": "human_review_required",
                            "migration_error": "conflicting legacy active Doctor task",
                        },
                        "$unset": {"active_key": ""},
                    },
                )
        if "active_repair_per_slug" in self.db.doctor_tasks.index_information():
            self.db.doctor_tasks.drop_index("active_repair_per_slug")
        if "active_doctor_task_per_entry_operation" in self.db.doctor_tasks.index_information():
            self.db.doctor_tasks.drop_index("active_doctor_task_per_entry_operation")
        self.db.doctor_tasks.create_index(
            "active_key",
            name="active_doctor_task_per_entry",
            unique=True,
            sparse=True,
        )

    def ready(self) -> bool:
        try:
            self.db.command("ping")
            return True
        except PyMongoError:
            return False

    def register(self, entry_id: str, businessname: str, address: str) -> dict:
        registration = Entry(entry_id=entry_id, businessname=businessname, address=address)
        entry_id = registration.entry_id
        businessname = registration.businessname
        address = registration.address
        if self.release_provider is None:
            raise RuntimeError("registration requires a spider-scripts release provider")
        base_release = self.release_provider().strip().lower()
        if re.fullmatch(r"[0-9a-f]{40}", base_release) is None:
            raise RuntimeError("release provider did not return a full Git commit SHA")
        now = datetime.now(UTC)
        active_key = entry_id
        with self._transaction() as session:
            kwargs = self._session_kwargs(session)
            existing_entry = self.db.entries.find_one(
                {"_id": entry_id},
                {"businessname": 1, "address": 1},
                **kwargs,
            )
            identity_changed = existing_entry is not None and (
                existing_entry.get("businessname") != businessname
                or existing_entry.get("address") != address
            )
            active_task = self.db.doctor_tasks.find_one(
                {"active_key": active_key},
                {"type": 1, "status": 1},
                **kwargs,
            )
            if identity_changed and active_task is not None and (
                active_task.get("type") != "create"
                or active_task.get("status") != "queued"
            ):
                raise RuntimeError(
                    "cannot correct registration while a non-queued create task is active"
                )
            self.db.entries.update_one(
                {"_id": entry_id},
                {
                    "$set": {
                        "entry_id": entry_id,
                        "businessname": businessname,
                        "address": address,
                        "updated_at": now,
                    },
                    "$setOnInsert": {"created_at": now},
                },
                upsert=True,
                **kwargs,
            )
            self.db.doctor_tasks.update_one(
                {"active_key": active_key},
                {
                    "$setOnInsert": {
                        "_id": str(uuid4()),
                        "active_key": active_key,
                        "entry_id": entry_id,
                        "type": "create",
                        "base_release": base_release,
                        "status": "queued",
                        "priority": 50,
                        "attempts": 0,
                        "max_attempts": 2,
                        "available_at": now,
                        "lease": None,
                        "created_at": now,
                        "updated_at": now,
                        "source_run_id": None,
                        "failure_class": None,
                        "errors": [],
                    }
                },
                upsert=True,
                **kwargs,
            )
            if identity_changed and active_task is not None:
                self.db.doctor_tasks.update_one(
                    {"active_key": active_key, "type": "create", "status": "queued"},
                    {
                        "$set": {
                            "base_release": base_release,
                            "attempts": 0,
                            "max_attempts": 2,
                            "available_at": now,
                            "lease": None,
                            "updated_at": now,
                            "source_run_id": None,
                            "failure_class": None,
                            "errors": [],
                        },
                        "$unset": {
                            "last_error": "",
                            "candidate_sha": "",
                            "candidate_result": "",
                            "result": "",
                        },
                    },
                    **kwargs,
                )
            task = self.db.doctor_tasks.find_one({"active_key": active_key}, **kwargs)
            if task is None:  # Defensive: the upsert and read share one transaction.
                raise RuntimeError("registered Doctor task could not be loaded")
        return {
            "entry_id": entry_id,
            "task_id": str(task["_id"]),
            "status": task["status"],
            "operation": task["type"],
        }

    def consume_doctor_handoff(self, task_id: str) -> ExecutionJob | None:
        task = self.db.doctor_tasks.find_one({"_id": task_id, "status": "succeeded"})
        if task is None:
            return None
        if task.get("handoff_job_id"):
            return self.get_job(str(task["handoff_job_id"]))
        result = task.get("result") or {}
        commit_sha = result.get("commit_sha")
        if not isinstance(commit_sha, str) or re.fullmatch(r"[0-9a-fA-F]{40}", commit_sha) is None:
            return None
        entry_contract = _doctor_entry_contract(result)
        commit_sha = commit_sha.lower()
        entry_id = task["entry_id"]
        activation = self.db.runtime_state.find_one({"_id": "activated_entry"})
        if activation is not None and activation.get("entry_id") != entry_id:
            raise RuntimeError("prototype supports only one activated entry")

        # Provisioning may fetch and fast-forward Git, so it must never run in a
        # MongoDB transaction. The provisioner is idempotent at an exact SHA.
        if self.provisioner is not None:
            self.provisioner(commit_sha)

        with self._transaction() as session:
            kwargs = self._session_kwargs(session)
            task = self.db.doctor_tasks.find_one(
                {"_id": task_id, "status": "succeeded"},
                **kwargs,
            )
            if task is None:
                return None
            if task.get("handoff_job_id"):
                return self.get_job(str(task["handoff_job_id"]))
            persisted_result = task.get("result") or {}
            persisted_sha = persisted_result.get("commit_sha")
            if not isinstance(persisted_sha, str) or persisted_sha.lower() != commit_sha:
                return None
            if _doctor_entry_contract(persisted_result) != entry_contract:
                raise RuntimeError("Doctor result metadata changed during handoff")
            activation = self.db.runtime_state.find_one({"_id": "activated_entry"}, **kwargs)
            if activation is not None and activation.get("entry_id") != entry_id:
                raise RuntimeError("prototype supports only one activated entry")
            entry_updates = {
                "scraper_release": commit_sha,
                "updated_at": datetime.now(UTC),
                **entry_contract,
            }
            if self.db.entries.update_one(
                {"_id": entry_id},
                {"$set": entry_updates},
                **kwargs,
            ).matched_count != 1:
                return None
            self.db.runtime_state.replace_one(
                {"_id": "activated_entry"},
                {"_id": "activated_entry", "entry_id": entry_id, "scraper_release": commit_sha},
                upsert=True,
                **kwargs,
            )
            job = ExecutionJob(
                entry_id=entry_id,
                idempotency_key=f"doctor-handoff:{task_id}:{commit_sha}",
                trigger="doctor_handoff",
                scraper_release=commit_sha,
            )
            self.db.execution_jobs.update_one(
                {"idempotency_key": job.idempotency_key},
                {"$setOnInsert": _encode(job)},
                upsert=True,
                **kwargs,
            )
            job_document = self.db.execution_jobs.find_one(
                {"idempotency_key": job.idempotency_key},
                **kwargs,
            )
            if job_document is None:
                raise RuntimeError("Doctor handoff job could not be loaded")
            handed_off_job = _decode(ExecutionJob, job_document, id_field=True)
            if handed_off_job is None:
                raise RuntimeError("Doctor handoff job could not be decoded")
            self.db.doctor_tasks.update_one(
                {"_id": task_id, "status": "succeeded"},
                {
                    "$set": {
                        "handoff_job_id": handed_off_job.id,
                        "handed_off_at": datetime.now(UTC),
                    },
                    "$unset": {"active_key": ""},
                },
                **kwargs,
            )
        return handed_off_job

    def consume_next_doctor_handoff(self) -> ExecutionJob | None:
        task = self.db.doctor_tasks.find_one(
            {"status": "succeeded", "handed_off_at": {"$exists": False}},
            sort=[("completed_at", ASCENDING), ("created_at", ASCENDING)],
        )
        if task is None:
            return None
        return self.consume_doctor_handoff(str(task["_id"]))

    def enqueue(self, job: ExecutionJob) -> ExecutionJob:
        entry = self.get_entry(job.entry_id)
        if entry is None or not entry.scraper_release:
            raise RuntimeError(f"entry {job.entry_id!r} has no activated scraper release")
        activation = self.db.runtime_state.find_one({"_id": "activated_entry"})
        if activation is None:
            raise RuntimeError(f"entry {job.entry_id!r} has no activated scraper release")
        if activation.get("entry_id") != job.entry_id:
            raise RuntimeError("prototype supports only one activated entry")
        if activation.get("scraper_release") != entry.scraper_release:
            raise RuntimeError(f"entry {job.entry_id!r} has no activated scraper release")
        job.scraper_release = entry.scraper_release
        return self.jobs.enqueue(job)

    def is_entry_release_activated(self, entry_id: str, release: str | None) -> bool:
        entry = self.get_entry(entry_id)
        if entry is None or not entry.scraper_release or release != entry.scraper_release:
            return False
        activation = self.db.runtime_state.find_one({"_id": "activated_entry"})
        return activation is not None and (
            activation.get("entry_id") == entry_id
            and activation.get("scraper_release") == release
        )

    def claim(self, worker_id: str) -> ExecutionJob | None:
        return self.jobs.claim(worker_id)

    def get_job(self, job_id: str) -> ExecutionJob | None:
        return self.jobs.get(job_id)

    def finish_job(self, job_id: str, lease_token: str, status) -> bool:
        return self.jobs.finish(job_id, lease_token, status)

    def put_entry(self, entry: Entry) -> Entry:
        now = datetime.now(UTC)
        document = _encode(entry, identifier=entry.entry_id)
        document.pop("_id")
        document["updated_at"] = now
        document.pop("created_at", None)
        self.db.entries.update_one(
            {"_id": entry.entry_id},
            {"$set": document, "$setOnInsert": {"created_at": entry.created_at}},
            upsert=True,
        )
        return self.get_entry(entry.entry_id)

    def get_entry(self, entry_id: str) -> Entry | None:
        return _decode(Entry, self.db.entries.find_one({"_id": entry_id}))

    def save_run(self, run: ExecutionRun) -> ExecutionRun:
        self.db.execution_runs.replace_one({"_id": run.id}, _encode(run), upsert=True)
        return run

    def list_runs(self, entry_id: str) -> list[ExecutionRun]:
        return [
            _decode(ExecutionRun, document, id_field=True)
            for document in self.db.execution_runs.find({"entry_id": entry_id}).sort("started_at", DESCENDING)
        ]

    def save_record(self, run_id: str, record: ScrapedRecord) -> str:
        record_id = str(uuid4())
        document = record.model_dump(mode="python")
        document.update({"_id": record_id, "run_id": run_id})
        self.db.records.insert_one(document)
        return record_id

    def get_record(self, record_id: str) -> ScrapedRecord | None:
        document = self.db.records.find_one({"_id": record_id})
        if document is None:
            return None
        document.pop("_id", None)
        document.pop("run_id", None)
        return ScrapedRecord.model_validate(document)

    def _upsert_doctor_task(
        self,
        entry_id: str,
        run_id: str,
        failure_class: str,
        errors: list[str],
        *,
        session=None,
    ) -> None:
        now = datetime.now(UTC)
        active_key = entry_id
        kwargs = self._session_kwargs(session)
        latest = {
            "source_run_id": run_id,
            "failure_class": failure_class,
            "errors": errors,
            "updated_at": now,
        }
        active = self.db.doctor_tasks.find_one({"active_key": active_key}, **kwargs)
        if active is not None:
            if active.get("type") == "repair" and active.get("status") == "queued":
                self.db.doctor_tasks.update_one({"_id": active["_id"]}, {"$set": latest}, **kwargs)
            return

        entry = self.db.entries.find_one({"_id": entry_id}, {"repair_attempts": 1}, **kwargs)
        repair_attempts = int((entry or {}).get("repair_attempts", 0))
        review_required = repair_attempts >= 2
        if not review_required:
            self.db.entries.update_one(
                {"_id": entry_id},
                {"$inc": {"repair_attempts": 1}, "$set": {"updated_at": now}},
                **kwargs,
            )
        self.db.doctor_tasks.update_one(
            {"active_key": active_key},
            {
                "$setOnInsert": {
                    "_id": str(uuid4()),
                    "active_key": active_key,
                    "entry_id": entry_id,
                    "type": "repair",
                    "status": "human_review_required" if review_required else "queued",
                    "repair_sequence": repair_attempts + 1,
                    "priority": 50,
                    "attempts": 0,
                    "max_attempts": 2,
                    "available_at": now,
                    "lease": None,
                    "created_at": now,
                    **latest,
                }
            },
            upsert=True,
            **kwargs,
        )

    def ensure_doctor_task(self, entry_id: str, run_id: str, failure_class: str, errors: list[str]) -> None:
        with self._transaction() as session:
            self._upsert_doctor_task(entry_id, run_id, failure_class, errors, session=session)

    def doctor_task_count(self) -> int:
        return self.db.doctor_tasks.count_documents({})

    # --- read-only console listings -----------------------------------------

    def list_entries(self) -> list[dict]:
        # View dicts, not Entry models: pre-contract entry documents lack
        # entry_id/businessname and must still be listable.
        return [
            {
                "id": str(document["_id"]),
                "businessname": document.get("businessname") or document.get("name"),
                "website": document.get("website"),
                "active": bool(document.get("active", True)),
                "scraper_release": document.get("scraper_release"),
                "created_at": document.get("created_at"),
                "updated_at": document.get("updated_at"),
            }
            for document in self.db.entries.find().sort("updated_at", DESCENDING)
        ]

    def list_recent_runs(self, limit: int = 50) -> list[ExecutionRun]:
        return [
            _decode(ExecutionRun, document, id_field=True)
            for document in self.db.execution_runs.find()
            .sort("started_at", DESCENDING)
            .limit(limit)
        ]

    def list_doctor_tasks(self, limit: int = 50) -> list[dict]:
        tasks = []
        for document in (
            self.db.doctor_tasks.find().sort("updated_at", DESCENDING).limit(limit)
        ):
            lease = document.get("lease")
            tasks.append(
                {
                    "id": str(document["_id"]),
                    "entry_id": document.get("entry_id"),
                    "type": document.get("type"),
                    "status": document.get("status"),
                    "attempts": int(document.get("attempts", 0)),
                    "max_attempts": int(document.get("max_attempts", 0)),
                    "failure_class": document.get("failure_class"),
                    "last_error": document.get("last_error"),
                    "candidate_sha": document.get("candidate_sha"),
                    "available_at": document.get("available_at"),
                    "created_at": document.get("created_at"),
                    "updated_at": document.get("updated_at"),
                    # The fencing token stays private to the Doctor.
                    "lease": {
                        "worker_id": lease.get("worker_id"),
                        "expires_at": lease.get("expires_at"),
                    }
                    if isinstance(lease, dict)
                    else None,
                }
            )
        return tasks

    def stats(self) -> dict:
        def by_status(collection) -> dict[str, int]:
            return {
                str(group["_id"]): int(group["count"])
                for group in collection.aggregate(
                    [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
                )
            }

        return {
            "entries": self.db.entries.count_documents({}),
            "records": self.db.records.count_documents({}),
            "doctor_tasks": by_status(self.db.doctor_tasks),
            "execution_jobs": by_status(self.db.execution_jobs),
            "execution_runs": by_status(self.db.execution_runs),
        }

    @contextmanager
    def _transaction(self):
        client = self.db.client
        if type(client).__module__.startswith("mongomock"):
            yield None
            return
        with client.start_session() as session, session.start_transaction():
            yield session

    @staticmethod
    def _session_kwargs(session) -> dict:
        return {"session": session} if session is not None else {}

    def complete_success(
        self,
        job: ExecutionJob,
        run: ExecutionRun,
        record: ScrapedRecord,
        artifact: Artifact,
    ) -> bool:
        if job.lease is None:
            return False
        with self._transaction() as session:
            kwargs = self._session_kwargs(session)
            result = self.db.execution_jobs.update_one(
                {
                    "_id": job.id,
                    "status": str(JobStatus.RUNNING),
                    "lease.token": job.lease.token,
                },
                {
                    "$set": {
                        "status": str(JobStatus.SUCCEEDED),
                        "lease": None,
                        "updated_at": datetime.now(UTC),
                    }
                },
                **kwargs,
            )
            if result.modified_count != 1:
                return False
            run.status = JobStatus.SUCCEEDED
            run.record_id = run.id
            run.finished_at = datetime.now(UTC)
            record_document = record.model_dump(mode="python")
            record_document.update({"_id": run.id, "run_id": run.id})
            self.db.records.replace_one({"_id": run.id}, record_document, upsert=True, **kwargs)
            self.db.execution_runs.replace_one({"_id": run.id}, _encode(run), upsert=True, **kwargs)
            artifact_document = artifact.model_dump(mode="python")
            artifact_document.update({"_id": run.id, "run_id": run.id})
            self.db.artifacts.replace_one({"_id": run.id}, artifact_document, upsert=True, **kwargs)
        return True

    def complete_failure(
        self,
        job: ExecutionJob,
        run: ExecutionRun,
        failure: FailureClass,
        errors: list[str],
    ) -> bool:
        if job.lease is None:
            return False
        with self._transaction() as session:
            kwargs = self._session_kwargs(session)
            result = self.db.execution_jobs.update_one(
                {
                    "_id": job.id,
                    "status": str(JobStatus.RUNNING),
                    "lease.token": job.lease.token,
                },
                {
                    "$set": {
                        "status": str(JobStatus.FAILED),
                        "lease": None,
                        "updated_at": datetime.now(UTC),
                    }
                },
                **kwargs,
            )
            if result.modified_count != 1:
                return False
            run.status = JobStatus.FAILED
            run.failure_class = failure
            run.errors = errors
            run.finished_at = datetime.now(UTC)
            self.db.execution_runs.replace_one({"_id": run.id}, _encode(run), upsert=True, **kwargs)
            if failure.doctor_eligible:
                self._upsert_doctor_task(
                    run.entry_id,
                    run.id,
                    str(failure),
                    errors,
                    session=session,
                )
        return True
