from __future__ import annotations

from typing import Protocol
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field

from spider_executor.models import (
    Entry,
    EntryId,

    ExecutionJob,
    ExecutionRun,
    ScrapedRecord,
)


class Control(Protocol):
    def ready(self) -> bool: ...
    def enqueue(self, job: ExecutionJob) -> ExecutionJob: ...
    def get_job(self, job_id: str) -> ExecutionJob | None: ...

    def get_entry(self, entry_id: str) -> Entry | None: ...
    def list_runs(self, entry_id: str) -> list[ExecutionRun]: ...
    def get_record(self, record_id: str) -> ScrapedRecord | None: ...
    def register(self, entry_id: str, businessname: str, address: str) -> dict: ...


class JobRequest(BaseModel):
    entry_id: str
    trigger: str = "manual"
    priority: int = 50
    idempotency_key: str | None = None


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entry_id: EntryId
    businessname: str = Field(min_length=1, max_length=256)
    address: str = Field(min_length=1, max_length=1000)


class RegisterResponse(BaseModel):
    entry_id: str
    task_id: str
    status: str
    operation: str


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

    @app.post("/api/v1/register", response_model=RegisterResponse, status_code=202)
    def register(request: RegisterRequest) -> dict:
        return control.register(request.entry_id, request.businessname, request.address)


    @app.get("/api/v1/entries/{entry_id}", response_model=Entry)
    def get_entry(entry_id: str) -> Entry:
        entry = control.get_entry(entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail="entry not found")
        return entry

    @app.get("/api/v1/entries/{entry_id}/runs", response_model=list[ExecutionRun])
    def list_runs(entry_id: str) -> list[ExecutionRun]:
        return control.list_runs(entry_id)

    @app.post("/api/v1/execution-jobs", response_model=ExecutionJob, status_code=201)
    def create_job(request: JobRequest) -> ExecutionJob:
        key = request.idempotency_key or f"{request.trigger}:{request.entry_id}:{uuid4()}"
        try:
            return control.enqueue(
                ExecutionJob(
                    entry_id=request.entry_id,
                    trigger=request.trigger,
                    priority=request.priority,
                    idempotency_key=key,
                )
            )
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

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
