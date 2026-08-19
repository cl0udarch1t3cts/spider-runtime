from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SPIDER_", env_file=".env", extra="ignore")

    mongodb_uri: str = "mongodb://localhost:27017/spider?replicaSet=rs0&directConnection=true"
    mongodb_database: str = "spider"
    scripts_root: Path = Path("/srv/spider/repositories/spider-scripts")
    scripts_remote_url: str = "https://github.com/cl0udarch1t3cts/spider-scripts.git"
    scripts_branch: str = "main"
    artifact_root: Path = Path("/srv/spider/artifacts")
    runtime_lock_path: Path = Path("/srv/spider/locks/scripts.lock")
    worker_id: str = "executor-1"
    worker_poll_seconds: float = 2.0
    runner_timeout_seconds: int = 90
    runner_url: str = "http://runner:8001"
