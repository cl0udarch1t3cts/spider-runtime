from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated, Any
from uuid import uuid4

from pydantic import BaseModel, Field, StringConstraints

# Upstream IDs are base64url-style and may start with "-"/"_" or contain inner
# spaces. Forbidden: a leading dot (dotfiles, ".."), an edge space, "/" anywhere
# - the ID becomes a single path segment under scrapers/ and tests/fixtures/.
EntryId = Annotated[
    str,
    Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_-](?:[A-Za-z0-9 ._-]*[A-Za-z0-9._-])?$"),
]
BusinessName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=256)]
BusinessAddress = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=1000)]


def utcnow() -> datetime:
    return datetime.now(UTC)


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    EXHAUSTED = "exhausted"


class FailureClass(StrEnum):
    NETWORK_TIMEOUT = "NETWORK_TIMEOUT"
    DNS_FAILURE = "DNS_FAILURE"
    HTTP_RATE_LIMIT = "HTTP_RATE_LIMIT"
    HTTP_DATACENTER_BLOCK = "HTTP_DATACENTER_BLOCK"
    HTTP_NOT_FOUND = "HTTP_NOT_FOUND"
    SECONDARY_PAGE_FAILURE = "SECONDARY_PAGE_FAILURE"
    SCRAPER_EXCEPTION = "SCRAPER_EXCEPTION"
    OUTPUT_SCHEMA_FAILURE = "OUTPUT_SCHEMA_FAILURE"
    SEMANTIC_VALIDATION_FAILURE = "SEMANTIC_VALIDATION_FAILURE"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    RELEASE_MISMATCH = "RELEASE_MISMATCH"
    SANDBOX_TIMEOUT = "SANDBOX_TIMEOUT"
    INACTIVE_ENTRY = "INACTIVE_ENTRY"
    UNKNOWN = "UNKNOWN"

    @property
    def doctor_eligible(self) -> bool:
        return self in {
            FailureClass.SCRAPER_EXCEPTION,
            FailureClass.OUTPUT_SCHEMA_FAILURE,
            FailureClass.SEMANTIC_VALIDATION_FAILURE,
            FailureClass.IDENTITY_MISMATCH,
        }


class Lease(BaseModel):
    worker_id: str
    token: str
    expires_at: datetime


class ExecutionJob(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    entry_id: EntryId
    idempotency_key: str
    trigger: str = "manual"
    priority: int = 50
    status: JobStatus = JobStatus.QUEUED
    attempts: int = 0
    max_attempts: int = 3
    available_at: datetime = Field(default_factory=utcnow)
    lease: Lease | None = None
    scraper_release: str | None = None
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class ScrapedField(BaseModel):
    value: Any = None
    source: str | None = None


class ScrapedRecord(BaseModel):
    entry_id: EntryId
    website: str | None = None
    fetched_at: datetime = Field(default_factory=utcnow)
    fields: dict[str, ScrapedField]
    errors: list[str] = Field(default_factory=list)


class ValidationResult(BaseModel):
    valid: bool
    non_null_field_count: int
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class EntryValidation(BaseModel):
    required_fields: list[str] = Field(default_factory=list)
    allowed_null_fields: list[str] = Field(default_factory=list)
    minimum_non_null_fields: int = 0
    allowed_source_hosts: list[str] = Field(default_factory=list)


class Entry(BaseModel):
    entry_id: EntryId
    businessname: BusinessName
    address: BusinessAddress = ""
    website: str | None = None
    active: bool = True
    scraper_release: str | None = None
    # Which model/provider built the activated scraper (ADR-008 audit).
    scraper_model: str | None = None
    scraper_provider: str | None = None
    validation: EntryValidation = Field(default_factory=EntryValidation)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class Artifact(BaseModel):
    key: str
    size_bytes: int
    sha256: str


class RunnerResult(BaseModel):
    exit_code: int
    record: ScrapedRecord
    output_artifact: Artifact
    stderr: str = ""
    scraper_release: str | None = None
    failure_class: FailureClass | None = None


class ExecutionRun(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    job_id: str
    entry_id: EntryId
    scraper_release: str | None = None
    scraper_model: str | None = None
    scraper_provider: str | None = None
    status: JobStatus
    failure_class: FailureClass | None = None
    record_id: str | None = None
    errors: list[str] = Field(default_factory=list)
    log_tail: str | None = None
    started_at: datetime = Field(default_factory=utcnow)
    finished_at: datetime | None = None
