from __future__ import annotations

import logging
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import ClassVar

logger = logging.getLogger(__name__)


class GitWorkspace:
    _GLOBAL_ALLOWED: ClassVar[set[str]] = {
        "PROGRESS.md",
        "registry.json",
        "tests/verify.py",
        "tests/test_verify.py",
    }

    def __init__(self, source_repository: Path, workspace_root: Path) -> None:
        self.source_repository = source_repository.resolve()
        self.workspace_root = workspace_root.resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        self._expected_heads: dict[Path, str] = {}

    @staticmethod
    def _run(cwd: Path, *args: str) -> str:
        return GitWorkspace._run_raw(cwd, *args).strip()

    @staticmethod
    def _run_raw(cwd: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.stdout

    def prepare(self, task_id: str, release: str) -> Path:
        if not re.fullmatch(r"[0-9a-f]{40}", release):
            raise ValueError("scraper release must be a full 40-character Git SHA")
        safe_id = re.sub(r"[^A-Za-z0-9_.-]", "-", task_id).strip("-.")
        if not safe_id:
            raise ValueError("task id cannot form a safe workspace name")
        workspace = self.workspace_root / safe_id
        if workspace.exists():
            shutil.rmtree(workspace)
        # Blobless partial clone: the full commit graph travels (rebases and
        # merge-base computations stay exact) but blobs are fetched on demand,
        # so historical file versions are never copied per task. The source
        # checkout is read-only, hence the permissive upload-pack is supplied
        # on the client side instead of via source repository config.
        permissive_upload_pack = (
            "git -c uploadpack.allowfilter=true -c uploadpack.allowanysha1inwant=true upload-pack"
        )
        subprocess.run(
            [
                "git",
                "clone",
                "--quiet",
                "--no-local",
                "--no-checkout",
                "--filter=blob:none",
                "--upload-pack",
                permissive_upload_pack,
                str(self.source_repository),
                str(workspace),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        # Lazy blob fetches (checkout below, later rebases while origin is
        # still the local path) need the same permissive upload-pack.
        self._run(workspace, "config", "remote.origin.uploadpack", permissive_upload_pack)
        self._configure_shared_file_merges(workspace)
        # Checkout while origin still points at the local source so the
        # release's blobs come from disk, not the network.
        self._run(workspace, "checkout", "--quiet", "--detach", release)
        if self._run(workspace, "rev-parse", "HEAD") != release:
            raise RuntimeError("workspace did not resolve to requested release")
        source_remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=self.source_repository,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if source_remote.returncode == 0 and source_remote.stdout.strip():
            # The real remote speaks stock upload-pack; drop the local override.
            self._run(workspace, "config", "--unset", "remote.origin.uploadpack")
            self._run(workspace, "remote", "set-url", "origin", source_remote.stdout.strip())
        if self._run(workspace, "status", "--porcelain", "--untracked-files=all"):
            raise RuntimeError("new Doctor workspace is unexpectedly dirty")
        self._expected_heads[workspace.resolve()] = release
        return workspace

    def _configure_shared_file_merges(self, workspace: Path) -> None:
        # Concurrent tasks all append to the shared tracking files; make
        # publication rebases merge them instead of conflicting. Workspace-local
        # config only — nothing is committed to the repository.
        (workspace / ".git" / "info").mkdir(parents=True, exist_ok=True)
        (workspace / ".git" / "info" / "attributes").write_text(
            "PROGRESS.md merge=union\nregistry.json merge=registryentries\n"
        )
        self._run(workspace, "config", "merge.registryentries.name", "registry entry union")
        self._run(
            workspace,
            "config",
            "merge.registryentries.driver",
            f"{sys.executable} -m spider_doctor.merge_registry %O %A %B",
        )

    def resume(self, task_id: str, candidate_sha: str) -> Path:
        if not re.fullmatch(r"[0-9a-f]{40}", candidate_sha):
            raise ValueError("candidate SHA must be a full 40-character Git SHA")
        safe_id = re.sub(r"[^A-Za-z0-9_.-]", "-", task_id).strip("-.")
        workspace = (self.workspace_root / safe_id).resolve()
        if not workspace.is_dir() or not (workspace / ".git").is_dir():
            raise RuntimeError("persisted Doctor candidate workspace is unavailable")
        # Workspaces persisted before the merge drivers existed retry their
        # publication here; give them the same conflict-free rebase setup.
        self._configure_shared_file_merges(workspace)
        if self._run(workspace, "rev-parse", "HEAD") != candidate_sha:
            # A crash between a publication rebase and candidate persistence can
            # leave HEAD on an unrecorded SHA (or mid-rebase). The recorded
            # candidate commit is still in the object store; restore it.
            subprocess.run(
                ["git", "rebase", "--abort"],
                cwd=workspace,
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self._run(workspace, "checkout", "--quiet", "--detach", candidate_sha)
            if self._run(workspace, "rev-parse", "HEAD") != candidate_sha:
                raise RuntimeError("persisted Doctor candidate workspace does not match candidate SHA")
        return workspace

    def validate_changes(self, workspace: Path, entry_id: str) -> list[str]:
        workspace = workspace.resolve()
        expected_head = self._expected_heads.get(workspace)
        if expected_head is None:
            raise ValueError("workspace was not prepared by this dispatcher")
        if self._run(workspace, "rev-parse", "HEAD") != expected_head:
            raise ValueError("workspace HEAD changed during Doctor execution")
        if not re.fullmatch(r"[A-Za-z0-9_-](?:[A-Za-z0-9 ._-]{0,126}[A-Za-z0-9._-])?", entry_id):
            raise ValueError("unsafe entry_id")
        output = self._run_raw(workspace, "status", "--porcelain=v1", "-z", "--untracked-files=all")
        changed: list[str] = []
        discarded: list[str] = []
        for entry in output.split("\0"):
            if not entry:
                continue
            if len(entry) < 4 or entry[2] != " ":
                raise ValueError("could not safely parse Git status output")
            status_code = entry[:2]
            if "R" in status_code or "C" in status_code:
                raise ValueError("renames and copies are not allowed in Doctor patches")
            name = entry[3:]
            path = PurePosixPath(name)
            fixture_allowed = path.parts[:3] == ("tests", "fixtures", entry_id)
            # Only code and metadata belong in the scraper directory; page
            # dumps and probe files Hermes leaves there are scratch, not
            # publishable content (fixtures have tests/fixtures/<entry_id>).
            scraper_allowed = path.parts[:2] == ("scrapers", entry_id) and path.suffix in {
                ".py",
                ".json",
            }
            allowed = (
                name in self._GLOBAL_ALLOWED
                or scraper_allowed
                or fixture_allowed
            )
            candidate = workspace / Path(*path.parts)
            safe = (
                not path.is_absolute()
                and ".." not in path.parts
                and candidate.parent.resolve().is_relative_to(workspace)
            )
            if safe and not allowed and status_code == "??":
                # Hermes routinely leaves scratch output (page caches, downloads)
                # in the workspace. Untracked files can never reach publication,
                # so discard them instead of failing the whole attempt; edits to
                # tracked files outside the allowlist still fail below.
                candidate.unlink(missing_ok=True)
                discarded.append(name)
                continue
            if not safe or not candidate.resolve().is_relative_to(workspace) or not allowed:
                raise ValueError(f"changed file is outside the Doctor allowlist: {name}")
            if candidate.exists() or candidate.is_symlink():
                metadata = candidate.lstat()
                if not stat.S_ISREG(metadata.st_mode):
                    raise ValueError(f"changed path is not a regular file: {name}")
                if metadata.st_size > 100 * 1024 * 1024:
                    raise ValueError(f"changed file exceeds size limit: {name}")
            changed.append(path.as_posix())
            if len(changed) > 1000:
                raise ValueError("Doctor patch changes too many files")
        if discarded:
            logger.warning(
                "discarded %d untracked scratch file(s) outside the Doctor allowlist: %s",
                len(discarded),
                ", ".join(sorted(discarded)[:20]),
            )
        return sorted(changed)
