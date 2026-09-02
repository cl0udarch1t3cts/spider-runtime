import socket
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SPIDER_", env_file=".env", extra="ignore")

    mongodb_uri: str = "mongodb://localhost:27017/spider?replicaSet=rs0&directConnection=true"
    mongodb_database: str = "spider"
    scripts_root: Path = Path("/srv/spider/repositories/spider-scripts")
    scripts_remote_url: str = "git@github.com:cl0udarch1t3cts/spider-scripts.git"
    scripts_branch: str = "main"
    artifact_root: Path = Path("/srv/spider/artifacts")
    runtime_lock_path: Path = Path("/srv/spider/locks/scripts.lock")
    # Per-replica identity so scaled workers (compose --scale worker=N) are
    # distinguishable in leases and logs; SPIDER_WORKER_ID still overrides.
    worker_id: str = Field(default_factory=lambda: f"executor-{socket.gethostname()}")
    worker_poll_seconds: float = 2.0
    # Concurrent scrapes from one worker process. Claims are atomic and each
    # run is its own sandboxed runner subprocess, so threads only overlap
    # network waiting, not scraper execution state.
    worker_concurrency: int = 1
    runner_timeout_seconds: int = 90
    runner_url: str = "http://runner:8001"
