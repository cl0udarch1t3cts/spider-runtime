from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Annotated, Any, Literal

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
    entry_id: str = Field(pattern=r"^[A-Za-z0-9_-](?:[A-Za-z0-9 ._-]{0,126}[A-Za-z0-9._-])?$")
    type: Literal["repair", "create"] = "repair"
    status: DoctorStatus = DoctorStatus.QUEUED
    priority: int = 50
    attempts: int = 0
    max_attempts: int = 2
    available_at: datetime = Field(default_factory=utcnow)
    source_run_id: str | None = None
    failure_class: str | None = None
    errors: list[str] = Field(default_factory=list)
    base_release: str | None = None
    candidate_sha: str | None = None
    candidate_result: dict[str, Any] | None = None
    lease: Lease | None = None
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


AgentChangedPath = Annotated[
    str,
    Field(
        pattern=r"^(?:/workspace/)?[^/].*$",
        description=(
            "Repository-relative POSIX path. The exact /workspace/ mount prefix "
            "is accepted for compatibility; other absolute paths and '..' are forbidden."
        ),
    ),
]


class DoctorResult(BaseModel):
    # Agent-authored results can request review or report failure. Only trusted
    # host code may transition the durable task to succeeded after validation,
    # candidate persistence, and publication.
    status: Literal[DoctorStatus.AWAITING_REVIEW, DoctorStatus.FAILED]
    summary: str
    changed_files: list[AgentChangedPath] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("status")
    @classmethod
    def terminal_agent_status(cls, value: DoctorStatus) -> DoctorStatus:
        if value not in {DoctorStatus.AWAITING_REVIEW, DoctorStatus.FAILED}:
            raise ValueError("agent result status must be awaiting_review or failed")
        return value

    @field_validator("changed_files", mode="before")
    @classmethod
    def safe_relative_paths(cls, values: Any) -> Any:
        if not isinstance(values, list):
            return values
        normalized: list[Any] = []
        for raw_value in values:
            if not isinstance(raw_value, str):
                normalized.append(raw_value)
                continue
            value = raw_value.removeprefix("/workspace/")
            path = PurePosixPath(value)
            if path.is_absolute() or not path.parts or ".." in path.parts:
                raise ValueError(f"unsafe changed file: {raw_value!r}")
            normalized.append(value)
        return normalized
