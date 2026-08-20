from __future__ import annotations

import argparse
import logging
import time
from datetime import timedelta

from pymongo import MongoClient

from spider_doctor.evidence import MongoEvidenceLoader
from spider_doctor.launcher import DockerHermesLauncher, LauncherConfig
from spider_doctor.publisher import TrustedGitPublisher
from spider_doctor.repository import MongoDoctorTaskRepository
from spider_doctor.settings import Settings
from spider_doctor.worker import DoctorWorker
from spider_doctor.workspace import GitWorkspace

logger = logging.getLogger(__name__)


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
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the isolated Hermes Script Doctor dispatcher")
    parser.add_argument("--once", action="store_true", help="process at most one task")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    settings = Settings()
    worker = create_worker(settings)
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
