from __future__ import annotations

import argparse
import subprocess

from pymongo import MongoClient

from spider_doctor.repository import MongoDoctorTaskRepository
from spider_doctor.settings import Settings


def _git(source, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Queue creation of a new deterministic scraper")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--address", required=True)
    parser.add_argument("--website")
    parser.add_argument("--priority", type=int, default=40)
    args = parser.parse_args()

    settings = Settings()
    source = settings.source_repository.resolve()
    if _git(source, "status", "--porcelain", "--untracked-files=all"):
        raise SystemExit("refusing to enqueue from a dirty spider-scripts checkout")
    release = _git(source, "rev-parse", "--verify", "HEAD^{commit}")
    client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
    repository = MongoDoctorTaskRepository(client[settings.mongodb_database].doctor_tasks)
    repository.ensure_indexes()
    task = repository.enqueue_create(
        slug=args.slug,
        name=args.name,
        address=args.address,
        website=args.website,
        base_release=release,
        priority=args.priority,
    )
    print(task.model_dump_json(by_alias=True))


if __name__ == "__main__":
    main()
