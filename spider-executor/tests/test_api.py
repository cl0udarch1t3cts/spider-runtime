from fastapi.testclient import TestClient

from spider_executor.api import create_app
from spider_executor.models import ExecutionJob


class FakeControl:
    def __init__(self) -> None:
        self.jobs = {}
        self.entries = {}
        self.runs = {}
        self.records = {}

    def ready(self) -> bool:
        return True

    def enqueue(self, job: ExecutionJob) -> ExecutionJob:
        self.jobs[job.id] = job
        return job

    def get_job(self, job_id: str):
        return self.jobs.get(job_id)

    def put_entry(self, entry):
        self.entries[entry.slug] = entry
        return entry

    def get_entry(self, slug):
        return self.entries.get(slug)

    def list_runs(self, slug):
        return [run for run in self.runs.values() if run.slug == slug]

    def get_record(self, record_id):
        return self.records.get(record_id)


def test_health_and_job_round_trip() -> None:
    app = create_app(FakeControl())
    client = TestClient(app)
    assert client.get("/health/live").json() == {"status": "ok"}
    assert client.get("/health/ready").status_code == 200

    response = client.post("/api/v1/execution-jobs", json={"slug": "example", "trigger": "manual"})
    assert response.status_code == 201
    job = response.json()
    fetched = client.get(f"/api/v1/execution-jobs/{job['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["slug"] == "example"


def test_entry_round_trip_and_empty_runs() -> None:
    app = create_app(FakeControl())
    client = TestClient(app)
    response = client.put(
        "/api/v1/entries/example",
        json={
            "name": "Example",
            "website": "https://example.com",
            "validation": {"required_fields": ["NAME"], "minimum_non_null_fields": 1},
        },
    )
    assert response.status_code == 200
    assert response.json()["slug"] == "example"
    assert client.get("/api/v1/entries/example").status_code == 200
    assert client.get("/api/v1/entries/example/runs").json() == []


def test_missing_record_returns_404() -> None:
    client = TestClient(create_app(FakeControl()))
    assert client.get("/api/v1/records/missing").status_code == 404
