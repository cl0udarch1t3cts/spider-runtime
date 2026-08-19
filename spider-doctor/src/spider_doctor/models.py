from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


def utcnow() -> datetime:
    return datetime.now(UTC)


class DoctorStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    AWAITING_REVIEW = "awaiting_review"
    FAILED = "failed"
    EXHAUSTED = "exhausted"
    SUCCEEDED = "succeeded"


class Lease(BaseModel):
    worker_id: str
    token: str
    expires_at: datetime


class DoctorTask(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id", pattern=r"^[A-Za-z0-9:._-]{1,255}$")
    entry_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
    type: Literal["repair", "create"] = "repair"
    status: DoctorStatus = DoctorStatus.QUEUED
    priority: int = 50
    attempts: int = 0
    max_attempts: int = 2
    available_at: datetime = Field(default_factory=utcnow)
    source_run_id: str | None = None
    failure_class: str = "NEW_SCRAPER"
    errors: list[str] = Field(default_factory=list)
    base_release: str | None = None
    candidate_sha: str | None = None
    candidate_result: dict[str, Any] | None = None
    lease: Lease | None = None
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class DoctorResult(BaseModel):
    status: DoctorStatus
    summary: str
    changed_files: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("status")
    @classmethod
    def terminal_agent_status(cls, value: DoctorStatus) -> DoctorStatus:
        if value not in {DoctorStatus.AWAITING_REVIEW, DoctorStatus.FAILED}:
            raise ValueError("agent result status must be awaiting_review or failed")
        return value

    @field_validator("changed_files")
    @classmethod
    def safe_relative_paths(cls, values: list[str]) -> list[str]:
        for value in values:
            path = PurePosixPath(value)
            if path.is_absolute() or not path.parts or ".." in path.parts:
                raise ValueError(f"unsafe changed file: {value!r}")
        return values
