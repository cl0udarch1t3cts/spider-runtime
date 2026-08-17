from __future__ import annotations

from urllib.parse import urlparse

from pydantic import BaseModel, Field

from spider_executor.models import ScrapedRecord, ValidationResult


class RecordExpectations(BaseModel):
    required_fields: list[str] = Field(default_factory=list)
    allowed_null_fields: list[str] = Field(default_factory=list)
    minimum_non_null_fields: int = 0
    allowed_source_hosts: list[str] = Field(default_factory=list)


def validate_record(record: ScrapedRecord, expectations: RecordExpectations) -> ValidationResult:
    errors: list[str] = []
    non_null = 0
    for name, field in record.fields.items():
        if field.value is None:
            if field.source is not None:
                errors.append(f"field {name} is null but has provenance")
            if name not in expectations.required_fields and name not in expectations.allowed_null_fields:
                errors.append(f"field {name} is null but is not allowed to be null")
            continue
        non_null += 1
        if not field.source:
            errors.append(f"field {name} has a value without provenance")
            continue
        parsed = urlparse(field.source)
        host = (parsed.hostname or "").lower()
        if parsed.scheme not in {"http", "https"} or not host:
            errors.append(f"field {name} source must be an absolute HTTP(S) URL")
            continue
        if expectations.allowed_source_hosts and host not in {
            h.lower() for h in expectations.allowed_source_hosts
        }:
            errors.append(f"field {name} source host {host} is not allowed")
    for name in expectations.required_fields:
        field = record.fields.get(name)
        if field is None or field.value is None:
            errors.append(f"required field {name} is null")
    if non_null < expectations.minimum_non_null_fields:
        errors.append(
            f"record has {non_null} non-null fields; minimum is {expectations.minimum_non_null_fields}"
        )
    errors.extend(record.errors)
    return ValidationResult(valid=not errors, non_null_field_count=non_null, errors=errors)
