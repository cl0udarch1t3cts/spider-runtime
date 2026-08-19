from pathlib import Path

from spider_executor.artifacts import LocalArtifactStore
from spider_executor.runner import SpiderRunner
from spider_executor.runner_api import create_runner_app
from spider_executor.settings import Settings

settings = Settings()
runner = SpiderRunner(
    settings.scripts_root,
    LocalArtifactStore(Path("/tmp/runner-artifacts")),
    timeout_seconds=settings.runner_timeout_seconds,
    runtime_lock_path=settings.runtime_lock_path,
)
app = create_runner_app(runner)
