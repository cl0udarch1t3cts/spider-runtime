from pathlib import Path

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SPIDER_DOCTOR_",
        env_file=".env",
        extra="ignore",
    )

    mongodb_uri: str = "mongodb://localhost:27017/spider?replicaSet=rs0&directConnection=true"
    mongodb_database: str = "spider"
    worker_id: str = "doctor-1"
    poll_seconds: float = Field(default=5.0, gt=0)
    lease_minutes: int = Field(default=40, ge=5, le=240)
    source_repository: Path = Path("../spider-scripts")
    workspace_root: Path = Path("./data/workspaces")
    task_root: Path = Path("./data/tasks")
    hermes_home: Path = Path("./data/hermes")
    hermes_image: str | None = None
    proxy_token_file: Path | None = None
    docker_binary: str = "docker"
    docker_network: str = "spider-doctor-egress"
    egress_proxy_url: str = "http://spider-doctor-egress-proxy:3128"
    publication_branch: str = "main"
    git_author_name: str = "Spider Doctor"
    git_author_email: str = "spider-doctor@localhost"
    agent_timeout_seconds: int = Field(default=1800, ge=60, le=7200)
    agent_max_turns: int = Field(default=40, ge=1, le=100)
    # Concurrent Hermes task launches. Size against host capacity: each task
    # container is capped at 2 CPUs / 4g, and the broker concurrency limit
    # must be at least this value.
    max_parallel_tasks: int = Field(default=2, ge=1, le=8)
    # Subscription budget gate: consulted before every Hermes launch. The
    # weekly contingent is paced at budget_daily_percent per day, capped so
    # budget_reserve_percent always stays free for interactive development.
    broker_usage_url: str | None = None
    budget_daily_percent: float = Field(default=10.0, gt=0, le=100)
    budget_reserve_percent: float = Field(default=30.0, ge=0, lt=100)
    budget_cache_seconds: int = Field(default=300, ge=10)
    budget_retry_minutes: int = Field(default=30, ge=1)

    @model_validator(mode="after")
    def lease_covers_agent_and_completion(self) -> "Settings":
        if self.lease_minutes * 60 < self.agent_timeout_seconds + 300:
            raise ValueError("Doctor lease must exceed the agent timeout by at least five minutes")
        return self
