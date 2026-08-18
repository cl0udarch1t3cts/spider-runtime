import subprocess
from datetime import UTC, datetime
from pathlib import Path

import mongomock

from spider_doctor.evidence import MongoEvidenceLoader
from spider_doctor.models import DoctorResult, DoctorStatus
from spider_doctor.repository import MongoDoctorTaskRepository
from spider_doctor.worker import DoctorWorker
from spider_doctor.workspace import GitWorkspace


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()


class RepairingAgent:
    def run(self, task, *, workspace, task_file, output_dir):
        scraper = workspace / "scrapers" / task.slug
        scraper.mkdir(parents=True)
        (scraper / "scrape.py").write_text("def scrape(record, ctx):\n    pass\n")
        return DoctorResult(
            status=DoctorStatus.AWAITING_REVIEW,
            summary="repair ready",
            changed_files=[f"scrapers/{task.slug}/scrape.py"],
            tests=["fixture test passed"],
        )


def test_repair_task_vertical_slice_reaches_awaiting_review(tmp_path: Path) -> None:
    source = tmp_path / "spider-scripts"
    source.mkdir()
    git(source, "init", "-q")
    (source / "AGENTS.md").write_text("Repair deterministic scrapers only.\n")
    git(source, "add", ".")
    git(source, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "base")
    release = git(source, "rev-parse", "HEAD")

    db = mongomock.MongoClient().spider
    now = datetime.now(UTC)
    db.entries.insert_one({"_id": "example", "name": "Example", "website": "https://example.com"})
    db.execution_runs.insert_one(
        {
            "_id": "job:1",
            "job_id": "job",
            "slug": "example",
            "scraper_release": release,
            "status": "failed",
            "errors": ["selector missing"],
        }
    )
    db.doctor_tasks.insert_one(
        {
            "_id": "task-1",
            "active_key": "example",
            "slug": "example",
            "type": "repair",
            "status": "queued",
            "priority": 50,
            "attempts": 0,
            "max_attempts": 2,
            "available_at": now,
            "source_run_id": "job:1",
            "failure_class": "SCRAPER_EXCEPTION",
            "errors": ["selector missing"],
            "lease": None,
            "created_at": now,
            "updated_at": now,
        }
    )
    repository = MongoDoctorTaskRepository(db.doctor_tasks)
    worker = DoctorWorker(
        repository,
        MongoEvidenceLoader(db),
        GitWorkspace(source, tmp_path / "workspaces"),
        RepairingAgent(),
        worker_id="doctor-1",
        task_root=tmp_path / "tasks",
    )

    result = worker.process_one()

    assert result.status == DoctorStatus.AWAITING_REVIEW
    task = db.doctor_tasks.find_one({"_id": "task-1"})
    assert task["status"] == "awaiting_review"
    assert task["lease"] is None
    assert task["result"]["changed_files"] == ["scrapers/example/scrape.py"]
