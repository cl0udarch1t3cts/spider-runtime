from __future__ import annotations

from typing import Protocol
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

from spider_executor.models import (
    Entry,
    EntryValidation,
    ExecutionJob,
    ExecutionRun,
    ScrapedRecord,
)


class Control(Protocol):
    def ready(self) -> bool: ...
    def enqueue(self, job: ExecutionJob) -> ExecutionJob: ...
    def get_job(self, job_id: str) -> ExecutionJob | None: ...
    def put_entry(self, entry: Entry) -> Entry: ...
    def get_entry(self, slug: str) -> Entry | None: ...
    def list_runs(self, slug: str) -> list[ExecutionRun]: ...
    def get_record(self, record_id: str) -> ScrapedRecord | None: ...


class JobRequest(BaseModel):
    slug: str
    trigger: str = "manual"
    priority: int = 50
    idempotency_key: str | None = None


class EntryRequest(BaseModel):
    name: str
    website: str
    active: bool = True
    scraper_release: str | None = None
    validation: EntryValidation = EntryValidation()


def create_app(control: Control) -> FastAPI:
    app = FastAPI(title="Spider Executor", version="0.1.0")

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready")
    def ready(response: Response) -> dict[str, str]:
        if not control.ready():
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {"status": "unavailable"}
        return {"status": "ok"}

    @app.put("/api/v1/entries/{slug}", response_model=Entry)
    def put_entry(slug: str, request: EntryRequest) -> Entry:
        return control.put_entry(Entry(slug=slug, **request.model_dump()))

    @app.get("/api/v1/entries/{slug}", response_model=Entry)
    def get_entry(slug: str) -> Entry:
        entry = control.get_entry(slug)
        if entry is None:
            raise HTTPException(status_code=404, detail="entry not found")
        return entry

    @app.get("/api/v1/entries/{slug}/runs", response_model=list[ExecutionRun])
    def list_runs(slug: str) -> list[ExecutionRun]:
        return control.list_runs(slug)

    @app.post("/api/v1/execution-jobs", response_model=ExecutionJob, status_code=201)
    def create_job(request: JobRequest) -> ExecutionJob:
        key = request.idempotency_key or f"{request.trigger}:{request.slug}:{uuid4()}"
        return control.enqueue(
            ExecutionJob(
                slug=request.slug,
                trigger=request.trigger,
                priority=request.priority,
                idempotency_key=key,
            )
        )

    @app.get("/api/v1/execution-jobs/{job_id}", response_model=ExecutionJob)
    def get_job(job_id: str) -> ExecutionJob:
        job = control.get_job(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="job not found")
        return job

    @app.get("/api/v1/records/{record_id}", response_model=ScrapedRecord)
    def get_record(record_id: str) -> ScrapedRecord:
        record = control.get_record(record_id)
        if record is None:
            raise HTTPException(status_code=404, detail="record not found")
        return record

    return app
