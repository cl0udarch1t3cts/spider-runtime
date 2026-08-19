from spider_executor.models import ScrapedRecord
from spider_executor.validation import RecordExpectations, validate_record


def record(fields: dict) -> ScrapedRecord:
    return ScrapedRecord(entry_id="example", website="https://example.com", fields=fields)


def test_accepts_required_fields_with_provenance() -> None:
    result = validate_record(
        record({"NAME": {"value": "Example", "source": "https://example.com"}}),
        RecordExpectations(required_fields=["NAME"], minimum_non_null_fields=1),
    )
    assert result.valid
    assert result.errors == []


def test_rejects_missing_required_field() -> None:
    result = validate_record(
        record({"NAME": {"value": None, "source": None}}),
        RecordExpectations(required_fields=["NAME"]),
    )
    assert not result.valid
    assert "required field NAME is null" in result.errors


def test_rejects_value_without_provenance() -> None:
    result = validate_record(
        record({"NAME": {"value": "Example", "source": None}}),
        RecordExpectations(required_fields=["NAME"]),
    )
    assert not result.valid
    assert "field NAME has a value without provenance" in result.errors


def test_rejects_relative_or_non_http_provenance() -> None:
    result = validate_record(
        record({"NAME": {"value": "Example", "source": "generated"}}),
        RecordExpectations(required_fields=["NAME"]),
    )
    assert not result.valid
    assert "field NAME source must be an absolute HTTP(S) URL" in result.errors


def test_rejects_null_field_not_explicitly_allowed() -> None:
    result = validate_record(
        record(
            {
                "NAME": {"value": "Example", "source": "https://example.com"},
                "MENU": {"value": None, "source": None},
            }
        ),
        RecordExpectations(required_fields=["NAME"]),
    )
    assert not result.valid
    assert "field MENU is null but is not allowed to be null" in result.errors


def test_accepts_explicitly_allowed_null_field() -> None:
    result = validate_record(
        record(
            {
                "NAME": {"value": "Example", "source": "https://example.com"},
                "MENU": {"value": None, "source": None},
            }
        ),
        RecordExpectations(required_fields=["NAME"], allowed_null_fields=["MENU"]),
    )
    assert result.valid


def test_rejects_unexpected_provenance_domain() -> None:
    result = validate_record(
        record({"NAME": {"value": "Wrong", "source": "https://evil.example/page"}}),
        RecordExpectations(required_fields=["NAME"], allowed_source_hosts=["example.com"]),
    )
    assert not result.valid
    assert "field NAME source host evil.example is not allowed" in result.errors
