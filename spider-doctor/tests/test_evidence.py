import mongomock
import pytest

from spider_doctor.evidence import MongoEvidenceLoader
from spider_doctor.models import DoctorTask


def test_loads_only_entry_scoped_failure_evidence() -> None:
    db = mongomock.MongoClient().spider
    db.entries.insert_one(
        {"_id": "entry-doc", "entry_id": "Entry_123", "businessname": "Example", "address": "Main 1"}
    )
    db.execution_runs.insert_one(
        {
            "_id": "job:1",
            "job_id": "job",
            "entry_id": "Entry_123",
            "scraper_release": "a" * 40,
            "status": "failed",
            "errors": ["traceback"],
        }
    )
    db.artifacts.insert_one(
        {"_id": "job:1", "run_id": "job:1", "key": "runs/job:1/output.json", "sha256": "b" * 64, "size_bytes": 10}
    )
    task = DoctorTask.model_validate(
        {
            "_id": "task",
            "entry_id": "Entry_123",
            "source_run_id": "job:1",
            "failure_class": "SCRAPER_EXCEPTION",
        }
    )

    evidence = MongoEvidenceLoader(db).load(task)

    assert evidence["scraper_release"] == "a" * 40
    assert evidence["entry"]["businessname"] == "Example"
    assert evidence["run"]["_id"] == "job:1"
    assert evidence["artifact"]["key"] == "runs/job:1/output.json"
    assert "mongodb" not in str(evidence).lower()
    assert "slug" not in evidence["task"]


def test_create_task_uses_base_release_and_authoritative_entry() -> None:
    db = mongomock.MongoClient().spider
    db.entries.insert_one(
        {"entry_id": "New.Place_1", "businessname": "Authoritative Name", "address": "Authoritative Address"}
    )
    task = DoctorTask.model_validate(
        {
            "_id": "create-task",
            "entry_id": "New.Place_1",
            "type": "create",
            "base_release": "c" * 40,
        }
    )

    evidence = MongoEvidenceLoader(db).load(task)

    assert evidence["scraper_release"] == "c" * 40
    assert evidence["entry"]["businessname"] == "Authoritative Name"
    assert evidence["entry"]["address"] == "Authoritative Address"
    assert evidence["run"] is None
    assert "slug" not in evidence["task"]


def test_repair_run_must_match_entry_id() -> None:
    db = mongomock.MongoClient().spider
    db.entries.insert_one({"entry_id": "safe", "businessname": "Safe", "address": "Here"})
    db.execution_runs.insert_one(
        {"_id": "run-1", "entry_id": "other", "scraper_release": "a" * 40}
    )
    task = DoctorTask.model_validate(
        {"_id": "task", "entry_id": "safe", "source_run_id": "run-1", "failure_class": "SCRAPER_EXCEPTION"}
    )

    with pytest.raises(ValueError, match="belongs to another entry"):
        MongoEvidenceLoader(db).load(task)
