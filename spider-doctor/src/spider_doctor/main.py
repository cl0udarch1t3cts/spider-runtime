from __future__ import annotations

import argparse
import logging
import signal
import time
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
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
    client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
    db = client[settings.mongodb_database]

    def budget_overrides() -> dict:
        # Console-set override in runtime_state; the gate validates the values
        # and falls back to the configured percents when absent or invalid.
        control = db.runtime_state.find_one({"_id": "doctor_control"}) or {}
        return {
            "daily_percent": control.get("daily_percent"),
            "reserve_percent": control.get("reserve_percent"),
        }

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
            overrides=budget_overrides,
        )
    repository = MongoDoctorTaskRepository(db.doctor_tasks)
    repository.ensure_indexes()

    def doctor_paused() -> bool:
        control = db.runtime_state.find_one({"_id": "doctor_control"})
        return bool(control and control.get("paused"))

    def model_policy() -> dict | None:
        # Console-editable per-attempt model routing (ADR-008); the worker
        # degrades to the configured codex model when this is absent or broken.
        return db.runtime_state.find_one({"_id": "model_policy"})

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
        pause_check=doctor_paused,
        model_policy=model_policy,
        codex_model=settings.model,
    )


def _run_forever(worker: DoctorWorker, settings: Settings) -> None:
    # Up to max_parallel_tasks claims run concurrently; claim leases, per-task
    # workspaces, and candidate rebasing already make concurrent tasks safe.
    pool = ThreadPoolExecutor(
        max_workers=settings.max_parallel_tasks, thread_name_prefix="doctor-task"
    )
    futures: set[Future] = set()
    try:
        while True:
            while len(futures) < settings.max_parallel_tasks:
                futures.add(pool.submit(worker.process_one))
            done, futures = wait(futures, return_when=FIRST_COMPLETED)
            processed = False
            for future in done:
                result = future.result()
                if result is not None:
                    processed = True
                    logger.info(
                        "Doctor attempt status=%s summary=%s", result.status, result.summary
                    )
            if not processed:
                time.sleep(settings.poll_seconds)
    finally:
        # On crash or SIGTERM stop claiming immediately; in-flight tasks keep
        # their leases and are reconciled by the next dispatcher start.
        pool.shutdown(wait=False, cancel_futures=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the isolated Hermes Script Doctor dispatcher")
    parser.add_argument("--once", action="store_true", help="process at most one task")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    signal.signal(signal.SIGTERM, _shutdown_on_signal)
    settings = Settings()
    worker = create_worker(settings)
    worker.launcher.reconcile_orphans()
    if args.once:
        result = worker.process_one()
        if result is not None:
            logger.info("Doctor attempt status=%s summary=%s", result.status, result.summary)
        return
    _run_forever(worker, settings)


if __name__ == "__main__":
    main()
