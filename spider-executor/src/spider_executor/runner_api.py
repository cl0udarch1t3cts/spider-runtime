from typing import Protocol

from fastapi import FastAPI
from pydantic import BaseModel, Field

from spider_executor.models import RunnerResult


class Runner(Protocol):
    def run(self, slug: str, run_id: str) -> RunnerResult: ...


class RunRequest(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,127}$")
    run_id: str = Field(pattern=r"^[A-Za-z0-9:._-]{1,255}$")


def create_runner_app(runner: Runner) -> FastAPI:
    app = FastAPI(title="Spider Isolated Runner", version="0.1.0")

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/run", response_model=RunnerResult)
    def run(request: RunRequest) -> RunnerResult:
        return runner.run(request.slug, request.run_id)

    return app
