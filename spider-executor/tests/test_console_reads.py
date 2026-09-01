"""Read-only listing endpoints consumed by the spider-console dashboard."""

from datetime import UTC, datetime, timedelta

import mongomock
from fastapi.testclient import TestClient

from spider_executor.api import create_app
from spider_executor.models import JobStatus
from spider_executor.service import MongoControlService


def seeded_service() -> MongoControlService:
    db = mongomock.MongoClient().spider
    service = MongoControlService(db)
    now = datetime.now(UTC)
    db.entries.insert_many(
        [
            {
                "_id": "entry-0",
                "entry_id": "entry-0",
                "businessname": "Business 0",
                "address": "Bern",
                "active": True,
                "scraper_release": "a" * 40,
                "created_at": now,
                "updated_at": now,
            },
            # Legacy shape without entry_id/businessname must not break listing.
            {
                "_id": "entry-legacy",
                "name": "Legacy Business",
                "slug": "entry-legacy",
                "active": True,
                "created_at": now,
                "updated_at": now + timedelta(minutes=1),
            },
        ]
    )
    for index in range(4):
        run = {
            "_id": f"job-{index}:1",
            "job_id": f"job-{index}",
            "entry_id": f"entry-{index % 2}",
            "scraper_release": "a" * 40,
            "status": "succeeded" if index % 2 == 0 else "failed",
            "failure_class": None,
            "record_id": None,
            "errors": [],
            "started_at": now + timedelta(minutes=index),
            "finished_at": now + timedelta(minutes=index, seconds=30),
        }
        if index == 0:
            # Legacy shape without entry_id must not break listing.
            del run["entry_id"]
        db.execution_runs.insert_one(run)
    db.records.insert_one({"_id": "job-0:1", "run_id": "job-0:1", "slug": "entry-0"})
    db.doctor_tasks.insert_many(
        [
            {
                "_id": "task-old",
                "entry_id": "entry-0",
                "type": "repair",
                "status": "succeeded",
                "attempts": 1,
                "max_attempts": 2,
                "created_at": now - timedelta(hours=2),
                "updated_at": now - timedelta(hours=2),
            },
            {
                "_id": "task-running",
                "entry_id": "entry-1",
                "type": "create",
                "status": "running",
                "attempts": 1,
                "max_attempts": 2,
                "failure_class": None,
                "last_error": "previous attempt failed",
                "lease": {
                    "worker_id": "doctor-1",
                    "token": "secret-fencing-token",
                    "expires_at": now + timedelta(minutes=30),
                },
                "created_at": now,
                "updated_at": now,
            },
        ]
    )
    db.execution_jobs.insert_one(
        {
            "_id": "job-0",
            "entry_id": "entry-0",
            "status": str(JobStatus.SUCCEEDED),
            "trigger": "manual",
            "priority": 50,
            "idempotency_key": "k",
            "created_at": now,
            "updated_at": now,
        }
    )
    return service


def test_service_lists_entries_most_recently_updated_first_tolerating_legacy_docs() -> None:
    service = seeded_service()

    entries = service.list_entries()

    assert [entry["id"] for entry in entries] == ["entry-legacy", "entry-0"]
    assert entries[0]["businessname"] == "Legacy Business"
    assert entries[1]["businessname"] == "Business 0"
    assert entries[1]["scraper_release"] == "a" * 40


def test_service_lists_recent_runs_across_entries_with_limit() -> None:
    service = seeded_service()

    runs = service.list_recent_runs(limit=2)

    assert [run["id"] for run in runs] == ["job-3:1", "job-2:1"]


def test_service_run_listing_tolerates_legacy_documents_without_entry_id() -> None:
    service = seeded_service()

    runs = service.list_recent_runs(limit=10)

    legacy = runs[-1]
    assert legacy["id"] == "job-0:1"
    assert legacy["entry_id"] is None
    assert legacy["status"] == "succeeded"


def test_service_lists_doctor_tasks_newest_first_without_lease_token() -> None:
    service = seeded_service()

    tasks = service.list_doctor_tasks(limit=10)

    assert [task["id"] for task in tasks] == ["task-running", "task-old"]
    running = tasks[0]
    assert running["lease"]["worker_id"] == "doctor-1"
    assert "token" not in running["lease"]
    assert running["last_error"] == "previous attempt failed"


def test_service_lists_only_unresolved_run_failures() -> None:
    db = mongomock.MongoClient().spider
    service = MongoControlService(db)
    now = datetime.now(UTC)
    db.execution_runs.insert_many(
        [
            # fixed later: failed run followed by a success for the same entry
            {"_id": "a:1", "entry_id": "entry-fixed", "status": "failed",
             "failure_class": "SCRAPER_EXCEPTION", "started_at": now - timedelta(hours=2)},
            {"_id": "a:2", "entry_id": "entry-fixed", "status": "succeeded",
             "started_at": now - timedelta(hours=1)},
            # still failing: latest run for the entry failed
            {"_id": "b:1", "entry_id": "entry-broken", "status": "succeeded",
             "started_at": now - timedelta(hours=2)},
            {"_id": "b:2", "entry_id": "entry-broken", "status": "failed",
             "failure_class": "NETWORK_TIMEOUT", "started_at": now - timedelta(minutes=30)},
            # healthy entry
            {"_id": "c:1", "entry_id": "entry-ok", "status": "succeeded",
             "started_at": now - timedelta(minutes=10)},
        ]
    )

    unresolved = service.list_recent_runs(limit=50, unresolved=True)

    assert [run["id"] for run in unresolved] == ["b:2"]
    assert unresolved[0]["entry_id"] == "entry-broken"


def test_service_filters_doctor_tasks_by_status() -> None:
    service = seeded_service()

    succeeded = service.list_doctor_tasks(limit=10, status="succeeded")
    running = service.list_doctor_tasks(limit=10, status="running")

    assert [task["id"] for task in succeeded] == ["task-old"]
    assert [task["id"] for task in running] == ["task-running"]


def test_service_stats_counts_by_status() -> None:
    service = seeded_service()

    stats = service.stats()

    assert stats["entries"] == 2
    assert stats["records"] == 1
    assert stats["doctor_tasks"] == {"succeeded": 1, "running": 1}
    assert stats["execution_jobs"] == {"succeeded": 1}
    assert stats["execution_runs"] == {"succeeded": 2, "failed": 2}


class ConsoleFakeControl:
    def __init__(self) -> None:
        self.now = datetime.now(UTC)
        self.requested_limits: list[int] = []
        self.requested_statuses: list[str | None] = []
        self.requested_unresolved: list[bool] = []

    def ready(self) -> bool:
        return True

    def list_entries(self):
        return [
            {
                "id": "entry-0",
                "businessname": "Business",
                "website": None,
                "active": True,
                "scraper_release": "a" * 40,
                "created_at": self.now,
                "updated_at": self.now,
            }
        ]

    def list_recent_runs(self, limit: int, unresolved: bool = False):
        self.requested_limits.append(limit)
        self.requested_unresolved.append(unresolved)
        return [
            {
                "id": "job-0:1",
                "job_id": "job-0",
                "entry_id": "entry-0",
                "scraper_release": "a" * 40,
                "status": "succeeded",
                "failure_class": None,
                "record_id": None,
                "errors": [],
                "started_at": self.now,
                "finished_at": None,
            }
        ]

    def list_doctor_tasks(self, limit: int, status: str | None = None):
        self.requested_limits.append(limit)
        self.requested_statuses.append(status)
        return [
            {
                "id": "task-running",
                "entry_id": "entry-0",
                "type": "repair",
                "status": "running",
                "attempts": 1,
                "max_attempts": 2,
                "last_error": None,
                "lease": {"worker_id": "doctor-1", "expires_at": self.now},
                "created_at": self.now,
                "updated_at": self.now,
            }
        ]

    def stats(self):
        return {
            "entries": 1,
            "records": 1,
            "doctor_tasks": {"running": 1},
            "execution_jobs": {},
            "execution_runs": {"succeeded": 1},
        }


def test_api_exposes_console_read_endpoints() -> None:
    control = ConsoleFakeControl()
    client = TestClient(create_app(control))

    entries = client.get("/api/v1/entries")
    runs = client.get("/api/v1/runs?limit=5")
    unresolved = client.get("/api/v1/runs?limit=5&unresolved=true")
    tasks = client.get("/api/v1/doctor-tasks?limit=7")
    filtered = client.get("/api/v1/doctor-tasks?limit=7&status=queued")
    stats = client.get("/api/v1/stats")

    assert entries.status_code == 200
    assert entries.json()[0]["id"] == "entry-0"
    assert runs.status_code == 200
    assert runs.json()[0]["id"] == "job-0:1"
    assert unresolved.status_code == 200
    assert control.requested_unresolved == [False, True]
    assert tasks.status_code == 200
    assert tasks.json()[0]["id"] == "task-running"
    assert filtered.status_code == 200
    assert stats.status_code == 200
    assert stats.json()["doctor_tasks"] == {"running": 1}
    assert control.requested_limits == [5, 5, 7, 7]
    assert control.requested_statuses == [None, "queued"]


def test_api_never_serializes_a_lease_token_even_if_control_leaks_one() -> None:
    class LeakyControl(ConsoleFakeControl):
        def list_doctor_tasks(self, limit: int, status: str | None = None):
            tasks = super().list_doctor_tasks(limit, status)
            tasks[0]["lease"]["token"] = "secret-fencing-token"
            return tasks

    response = TestClient(create_app(LeakyControl())).get("/api/v1/doctor-tasks")

    assert response.status_code == 200
    assert "secret-fencing-token" not in response.text


def test_api_bounds_console_listing_limits() -> None:
    client = TestClient(create_app(ConsoleFakeControl()))

    assert client.get("/api/v1/runs?limit=0").status_code == 422
    assert client.get("/api/v1/runs?limit=201").status_code == 422
    assert client.get("/api/v1/doctor-tasks?limit=201").status_code == 422


def test_doctor_pause_flag_round_trip_and_stats_exposure() -> None:
    service = seeded_service()

    assert service.doctor_paused() is False
    service.set_doctor_paused(True)
    assert service.doctor_paused() is True
    assert service.stats()["doctor_paused"] is True
    service.set_doctor_paused(False)
    assert service.doctor_paused() is False
    assert service.stats()["doctor_paused"] is False


def test_api_exposes_doctor_pause_control() -> None:
    class PausableControl(ConsoleFakeControl):
        paused = False

        def doctor_paused(self):
            return self.paused

        def set_doctor_paused(self, paused: bool):
            self.paused = paused
            return paused

    control = PausableControl()
    client = TestClient(create_app(control))

    assert client.get("/api/v1/doctor-control").json() == {"paused": False}
    response = client.put("/api/v1/doctor-control", json={"paused": True})
    assert response.status_code == 200
    assert response.json() == {"paused": True}
    assert control.paused is True
    assert client.put("/api/v1/doctor-control", json={"paused": False}).json() == {
        "paused": False
    }
    assert client.put("/api/v1/doctor-control", json={}).status_code == 422
