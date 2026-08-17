import json

import httpx
from fastapi.testclient import TestClient

from spider_executor.models import Artifact, RunnerResult, ScrapedRecord
from spider_executor.remote_runner import HttpSpiderRunner
from spider_executor.runner_api import create_runner_app


class FakeRunner:
    def run(self, slug: str, run_id: str) -> RunnerResult:
        return RunnerResult(
            exit_code=0,
            record=ScrapedRecord(slug=slug, fields={}),
            output_artifact=Artifact(key=f"runs/{run_id}/output.json", size_bytes=1, sha256="0" * 64),
            scraper_release="abc123",
        )


def test_runner_api_returns_structured_result() -> None:
    response = TestClient(create_runner_app(FakeRunner())).post(
        "/run", json={"slug": "example", "run_id": "job:1"}
    )
    assert response.status_code == 200
    assert response.json()["scraper_release"] == "abc123"


def test_http_runner_rejects_oversized_response() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, content=b"x" * 200, request=request)
    )
    runner = HttpSpiderRunner(
        "http://runner:8001", client=httpx.Client(transport=transport), max_response_bytes=100
    )
    result = runner.run("example", "job:1")
    assert result.failure_class.value == "OUTPUT_SCHEMA_FAILURE"


def test_http_runner_parses_valid_response() -> None:
    payload = FakeRunner().run("example", "job:1").model_dump(mode="json")
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, content=json.dumps(payload).encode(), request=request)
    )
    runner = HttpSpiderRunner("http://runner:8001", client=httpx.Client(transport=transport))
    assert runner.run("example", "job:1").scraper_release == "abc123"
