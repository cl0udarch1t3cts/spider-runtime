from __future__ import annotations

from contextlib import contextmanager
from datetime import UTC, datetime
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


class MongoControlService:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.jobs = MongoJobRepository(db.execution_jobs)

    def ensure_indexes(self) -> None:
        self.jobs.ensure_indexes()
        self.db.execution_runs.create_index([("slug", ASCENDING), ("started_at", DESCENDING)])
        self.db.records.create_index("run_id", unique=True)
        self.db.artifacts.create_index("run_id", unique=True)
        self.db.doctor_tasks.create_index(
            "active_key",
            name="active_repair_per_slug",
            unique=True,
            sparse=True,
        )

    def ready(self) -> bool:
        try:
            self.db.command("ping")
            return True
        except PyMongoError:
            return False

    def enqueue(self, job: ExecutionJob) -> ExecutionJob:
        return self.jobs.enqueue(job)

    def claim(self, worker_id: str) -> ExecutionJob | None:
        return self.jobs.claim(worker_id)

    def get_job(self, job_id: str) -> ExecutionJob | None:
        return self.jobs.get(job_id)

    def finish_job(self, job_id: str, lease_token: str, status) -> bool:
        return self.jobs.finish(job_id, lease_token, status)

    def put_entry(self, entry: Entry) -> Entry:
        now = datetime.now(UTC)
        document = _encode(entry, identifier=entry.slug)
        document.pop("_id")
        document["updated_at"] = now
        document.pop("created_at", None)
        self.db.entries.update_one(
            {"_id": entry.slug},
            {"$set": document, "$setOnInsert": {"created_at": entry.created_at}},
            upsert=True,
        )
        return self.get_entry(entry.slug)

    def get_entry(self, slug: str) -> Entry | None:
        return _decode(Entry, self.db.entries.find_one({"_id": slug}))

    def save_run(self, run: ExecutionRun) -> ExecutionRun:
        self.db.execution_runs.replace_one({"_id": run.id}, _encode(run), upsert=True)
        return run

    def list_runs(self, slug: str) -> list[ExecutionRun]:
        return [
            _decode(ExecutionRun, document, id_field=True)
            for document in self.db.execution_runs.find({"slug": slug}).sort("started_at", DESCENDING)
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
        slug: str,
        run_id: str,
        failure_class: str,
        errors: list[str],
        *,
        session=None,
    ) -> None:
        now = datetime.now(UTC)
        kwargs = self._session_kwargs(session)
        latest = {
            "source_run_id": run_id,
            "failure_class": failure_class,
            "errors": errors,
            "updated_at": now,
        }
        queued = self.db.doctor_tasks.update_one(
            {"active_key": slug, "status": "queued"},
            {"$set": latest},
            **kwargs,
        )
        if queued.matched_count:
            return
        self.db.doctor_tasks.update_one(
            {"active_key": slug},
            {
                "$setOnInsert": {
                    "_id": str(uuid4()),
                    "active_key": slug,
                    "slug": slug,
                    "type": "repair",
                    "status": "queued",
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

    def ensure_doctor_task(self, slug: str, run_id: str, failure_class: str, errors: list[str]) -> None:
        self._upsert_doctor_task(slug, run_id, failure_class, errors)

    def doctor_task_count(self) -> int:
        return self.db.doctor_tasks.count_documents({})

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
                    run.slug,
                    run.id,
                    str(failure),
                    errors,
                    session=session,
                )
        return True
