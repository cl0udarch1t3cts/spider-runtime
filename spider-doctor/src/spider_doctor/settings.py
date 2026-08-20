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

    @model_validator(mode="after")
    def lease_covers_agent_and_completion(self) -> "Settings":
        if self.lease_minutes * 60 < self.agent_timeout_seconds + 300:
            raise ValueError("Doctor lease must exceed the agent timeout by at least five minutes")
        return self
