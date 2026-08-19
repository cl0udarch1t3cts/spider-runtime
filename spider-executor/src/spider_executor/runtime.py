from __future__ import annotations

import fcntl
import re
import subprocess
from pathlib import Path

from pymongo import MongoClient

from spider_executor.service import MongoControlService
from spider_executor.settings import Settings


def _git(repository: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-c", f"safe.directory={repository.resolve()}", *args],
        cwd=repository,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {completed.stderr[-4000:]}")
    return completed.stdout.strip()


def current_scripts_release(repository: Path) -> str:
    release = _git(repository, "rev-parse", "HEAD^{commit}")
    if re.fullmatch(r"[0-9a-f]{40}", release) is None:
        raise RuntimeError("spider-scripts did not resolve to an exact Git commit")
    return release


def provision_scripts(
    repository: Path,
    release: str,
    *,
    remote: str = "origin",
    branch: str = "main",
    lock_path: Path | None = None,
) -> None:
    repository = repository.resolve()
    if re.fullmatch(r"[0-9a-f]{40}", release) is None:
        raise ValueError("provisioning requires an exact Git commit SHA")
    git_dir = repository / ".git"
    if not git_dir.is_dir():
        raise RuntimeError("spider-scripts checkout has no Git metadata")
    lock_path = (lock_path or (git_dir / "spider-runtime.lock")).resolve()
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        if _git(repository, "status", "--porcelain", "--untracked-files=all"):
            raise RuntimeError("refusing to provision a dirty spider-scripts checkout")
        if current_scripts_release(repository) == release:
            return
        _git(repository, "fetch", remote, f"refs/heads/{branch}")
        fetched = _git(repository, "rev-parse", "FETCH_HEAD^{commit}")
        published = subprocess.run(
            ["git", "merge-base", "--is-ancestor", release, fetched],
            cwd=repository,
            timeout=30,
            check=False,
        )
        if published.returncode != 0:
            raise RuntimeError(f"Doctor commit {release} is not published on {remote}/{branch}")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", "HEAD", release],
            cwd=repository,
            timeout=30,
            check=False,
        )
        if ancestor.returncode != 0:
            raise RuntimeError("Doctor commit is not a fast-forward of the provisioned scripts checkout")
        _git(repository, "merge", "--ff-only", release)
        if current_scripts_release(repository) != release:
            raise RuntimeError("spider-scripts provisioning did not activate the requested commit")


def create_control(settings: Settings) -> MongoControlService:
    client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
    scripts_root = settings.scripts_root.resolve()
    service = MongoControlService(
        client[settings.mongodb_database],
        release_provider=lambda: current_scripts_release(scripts_root),
        provisioner=lambda release: provision_scripts(
            scripts_root,
            release,
            remote=settings.scripts_remote_url,
            branch=settings.scripts_branch,
            lock_path=settings.runtime_lock_path,
        ),
    )
    service.ensure_indexes()
    return service
