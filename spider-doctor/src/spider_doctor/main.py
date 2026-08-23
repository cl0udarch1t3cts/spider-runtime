from __future__ import annotations

import argparse
import logging
import signal
import time
from datetime import timedelta

from pymongo import MongoClient

from spider_doctor.budget import SubscriptionBudgetGate
from spider_doctor.evidence import MongoEvidenceLoader
from spider_doctor.launcher import DockerHermesLauncher, LauncherConfig
from spider_doctor.publisher import TrustedGitPublisher
from spider_doctor.repository import MongoDoctorTaskRepository
from spider_doctor.settings import Settings
from spider_doctor.worker import DoctorWorker
from spider_doctor.workspace import GitWorkspace

logger = logging.getLogger(__name__)


def _shutdown_on_signal(signum, _frame) -> None:
    raise SystemExit(128 + signum)


def create_worker(settings: Settings) -> DoctorWorker:
    source = settings.source_repository.resolve()
    hermes_home = settings.hermes_home.resolve()
    if not (source / ".git").exists():
        raise RuntimeError(f"spider-scripts repository is unavailable: {source}")
    if not hermes_home.is_dir():
        raise RuntimeError(
            f"Hermes Doctor home is unavailable: {hermes_home}; initialize it with the official image first"
        )
    if not settings.hermes_image:
        raise RuntimeError("SPIDER_DOCTOR_HERMES_IMAGE must be set to an image pinned by digest")
    budget_gate = None
    if settings.broker_usage_url:
        if settings.proxy_token_file is None:
            raise RuntimeError(
                "SPIDER_DOCTOR_PROXY_TOKEN_FILE is required to query the broker usage endpoint"
            )
        budget_gate = SubscriptionBudgetGate(
            settings.broker_usage_url,
            settings.proxy_token_file.read_text().strip(),
            daily_percent=settings.budget_daily_percent,
            reserve_percent=settings.budget_reserve_percent,
            cache_seconds=settings.budget_cache_seconds,
        )
    client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
    db = client[settings.mongodb_database]
    repository = MongoDoctorTaskRepository(db.doctor_tasks)
    repository.ensure_indexes()
    return DoctorWorker(
        repository,
        MongoEvidenceLoader(db),
        GitWorkspace(source, settings.workspace_root),
        DockerHermesLauncher(
            LauncherConfig(
                image=settings.hermes_image,
                hermes_home=hermes_home,
                proxy_token_file=settings.proxy_token_file,
                docker_binary=settings.docker_binary,
                network=settings.docker_network,
                egress_proxy_url=settings.egress_proxy_url,
                timeout_seconds=settings.agent_timeout_seconds,
                max_turns=settings.agent_max_turns,
            )
        ),
        TrustedGitPublisher(
            branch=settings.publication_branch,
            author_name=settings.git_author_name,
            author_email=settings.git_author_email,
        ),
        worker_id=settings.worker_id,
        task_root=settings.task_root,
        lease_for=timedelta(minutes=settings.lease_minutes),
        budget_gate=budget_gate,
        budget_retry_after=timedelta(minutes=settings.budget_retry_minutes),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the isolated Hermes Script Doctor dispatcher")
    parser.add_argument("--once", action="store_true", help="process at most one task")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    signal.signal(signal.SIGTERM, _shutdown_on_signal)
    settings = Settings()
    worker = create_worker(settings)
    worker.launcher.reconcile_orphans()
    while True:
        result = worker.process_one()
        if result is not None:
            logger.info("Doctor attempt status=%s summary=%s", result.status, result.summary)
        if args.once:
            return
        if result is None:
            time.sleep(settings.poll_seconds)


if __name__ == "__main__":
    main()
