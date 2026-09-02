from __future__ import annotations

import argparse
import logging
import time
from concurrent.futures import ThreadPoolExecutor

from spider_executor.artifacts import LocalArtifactStore
from spider_executor.remote_runner import HttpSpiderRunner
from spider_executor.runtime import create_control, release_contains
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
    scripts_root = settings.scripts_root.resolve()
    worker = ExecutorWorker(
        service,
        runner,
        worker_id=settings.worker_id,
        artifacts=artifacts,
        release_contains=lambda ancestor, descendant: release_contains(
            scripts_root, ancestor, descendant
        ),
    )
    def loop() -> None:
        while True:
            run = worker.process_one()
            if run is not None:
                logger.info(
                    "processed entry_id=%s run_id=%s status=%s", run.entry_id, run.id, run.status
                )
            if args.once:
                return
            if run is None:
                time.sleep(settings.worker_poll_seconds)

    concurrency = 1 if args.once else max(1, settings.worker_concurrency)
    if concurrency == 1:
        loop()
        return
    # Threads only overlap the HTTP wait on the runner; every claim is an
    # atomic, leased Mongo operation, so slots never share a job.
    logger.info("worker starting %d concurrent scrape slots", concurrency)
    with ThreadPoolExecutor(max_workers=concurrency, thread_name_prefix="scrape") as pool:
        for _ in range(concurrency):
            pool.submit(loop)


if __name__ == "__main__":
    main()
