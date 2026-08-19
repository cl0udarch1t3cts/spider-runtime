from __future__ import annotations

import argparse
import logging
import time

from spider_executor.artifacts import LocalArtifactStore
from spider_executor.remote_runner import HttpSpiderRunner
from spider_executor.runtime import create_control
from spider_executor.settings import Settings
from spider_executor.worker import ExecutorWorker

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Spider Executor worker")
    parser.add_argument("--once", action="store_true", help="process at most one job")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    settings = Settings()
    service = create_control(settings)
    artifacts = LocalArtifactStore(settings.artifact_root)
    runner = HttpSpiderRunner(
        settings.runner_url,
        timeout_seconds=settings.runner_timeout_seconds + 30,
    )
    worker = ExecutorWorker(
        service,
        runner,
        worker_id=settings.worker_id,
        artifacts=artifacts,
    )
    while True:
        run = worker.process_one()
        if run is not None:
            logger.info("processed entry_id=%s run_id=%s status=%s", run.entry_id, run.id, run.status)
        if args.once:
            return
        if run is None:
            time.sleep(settings.worker_poll_seconds)


if __name__ == "__main__":
    main()
