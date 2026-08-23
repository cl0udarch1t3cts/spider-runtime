import pytest
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
        self.entries[entry.entry_id] = entry
        return entry

    def get_entry(self, entry_id):
        return self.entries.get(entry_id)

    def list_runs(self, entry_id):
        return [run for run in self.runs.values() if run.entry_id == entry_id]

    def get_record(self, record_id):
        return self.records.get(record_id)

    def register(self, entry_id, businessname, address):
        self.entries[entry_id] = {
            "entry_id": entry_id,
            "businessname": businessname,
            "address": address,
        }
        return {
            "entry_id": entry_id,
            "task_id": "create-task",
            "status": "queued",
            "operation": "create",
        }


def test_register_accepts_exact_contract_asynchronously() -> None:
    client = TestClient(create_app(FakeControl()))

    response = client.post(
        "/api/v1/register",
        json={"entry_id": "business-123", "businessname": "Example AG", "address": "Bern"},
    )

    assert response.status_code == 202
    assert response.json() == {
        "entry_id": "business-123",
        "task_id": "create-task",
        "status": "queued",
        "operation": "create",
    }


def test_register_rejects_fields_outside_exact_contract() -> None:
    client = TestClient(create_app(FakeControl()))

    response = client.post(
        "/api/v1/register",
        json={
            "entry_id": "business-123",
            "businessname": "Example AG",
            "address": "Bern",
            "slug": "example",
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize("entry_id", ["../escape", "nested/path", ".", "", "x" * 129])
def test_register_rejects_unsafe_entry_id(entry_id: str) -> None:
    response = TestClient(create_app(FakeControl())).post(
        "/api/v1/register",
        json={"entry_id": entry_id, "businessname": "Example AG", "address": "Bern"},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("field", "value"),
    [("businessname", "x" * 257), ("address", "x" * 1001)],
)
def test_register_bounds_business_text(field: str, value: str) -> None:
    payload = {"entry_id": "business-123", "businessname": "Example AG", "address": "Bern"}
    payload[field] = value

    response = TestClient(create_app(FakeControl())).post("/api/v1/register", json=payload)

    assert response.status_code == 422


def test_health_and_job_round_trip() -> None:
    app = create_app(FakeControl())
    client = TestClient(app)
    assert client.get("/health/live").json() == {"status": "ok"}
    assert client.get("/health/ready").status_code == 200

    response = client.post("/api/v1/execution-jobs", json={"entry_id": "example", "trigger": "manual"})
    assert response.status_code == 201
    job = response.json()
    fetched = client.get(f"/api/v1/execution-jobs/{job['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["entry_id"] == "example"


def test_execution_job_rejects_entry_without_activated_release() -> None:
    class UnactivatedControl(FakeControl):
        def enqueue(self, job: ExecutionJob) -> ExecutionJob:
            raise RuntimeError(f"entry {job.entry_id!r} has no activated scraper release")

    response = TestClient(create_app(UnactivatedControl())).post(
        "/api/v1/execution-jobs",
        json={"entry_id": "example", "trigger": "manual"},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "entry 'example' has no activated scraper release"}


def test_registered_entry_round_trip_and_empty_runs() -> None:
    app = create_app(FakeControl())
    client = TestClient(app)
    response = client.post(
        "/api/v1/register",
        json={"entry_id": "example", "businessname": "Example", "address": "Bern"},
    )
    assert response.status_code == 202
    assert response.json()["entry_id"] == "example"
    assert client.get("/api/v1/entries/example").status_code == 200
    assert client.get("/api/v1/entries/example/runs").json() == []


def test_public_entry_mutation_route_is_unavailable() -> None:
    response = TestClient(create_app(FakeControl())).put(
        "/api/v1/entries/example",
        json={"entry_id": "example", "businessname": "Bypass", "address": "Bern"},
    )

    assert response.status_code == 405


def test_missing_record_returns_404() -> None:
    client = TestClient(create_app(FakeControl()))
    assert client.get("/api/v1/records/missing").status_code == 404
