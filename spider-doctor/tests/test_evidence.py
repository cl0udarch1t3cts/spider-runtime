import mongomock

from spider_doctor.evidence import MongoEvidenceLoader
from spider_doctor.models import DoctorTask


def test_loads_only_task_scoped_failure_evidence() -> None:
    db = mongomock.MongoClient().spider
    db.entries.insert_one({"_id": "example", "name": "Example", "website": "https://example.com", "active": True})
    db.execution_runs.insert_one(
        {
            "_id": "job:1",
            "job_id": "job",
            "slug": "example",
            "scraper_release": "a" * 40,
            "status": "failed",
            "errors": ["traceback"],
        }
    )
    db.artifacts.insert_one({"_id": "job:1", "run_id": "job:1", "key": "runs/job:1/output.json", "sha256": "b" * 64, "size_bytes": 10})
    task = DoctorTask.model_validate(
        {
            "_id": "task",
            "slug": "example",
            "source_run_id": "job:1",
            "failure_class": "SCRAPER_EXCEPTION",
        }
    )

    evidence = MongoEvidenceLoader(db).load(task)

    assert evidence["scraper_release"] == "a" * 40
    assert evidence["entry"]["name"] == "Example"
    assert evidence["run"]["_id"] == "job:1"
    assert evidence["artifact"]["key"] == "runs/job:1/output.json"
    assert "mongodb" not in str(evidence).lower()


def test_create_task_uses_pinned_base_release_without_a_failed_run() -> None:
    db = mongomock.MongoClient().spider
    task = DoctorTask.model_validate(
        {
            "_id": "create-task",
            "slug": "new-place",
            "type": "create",
            "scraper_release": "c" * 40,
            "request": {
                "name": "New Place",
                "address": "Main Street 1, 8000 Zürich",
            },
        }
    )

    evidence = MongoEvidenceLoader(db).load(task)

    assert evidence["scraper_release"] == "c" * 40
    assert evidence["entry"] is None
    assert evidence["run"] is None
    assert evidence["task"]["request"]["name"] == "New Place"
