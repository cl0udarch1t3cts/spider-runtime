from __future__ import annotations

import re
import subprocess
from pathlib import Path, PurePosixPath


class TrustedGitPublisher:
    """Host-only publisher; never mounted or invoked inside Hermes."""

    def __init__(
        self,
        *,
        branch: str,
        author_name: str,
        author_email: str,
        remote: str = "origin",
    ) -> None:
        if (
            not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,254}", branch)
            or ".." in branch
            or branch.endswith(("/", "."))
        ):
            raise ValueError("unsafe publication branch")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", remote):
            raise ValueError("unsafe publication remote")
        if not author_name.strip() or not author_email.strip():
            raise ValueError("publisher Git identity is required")
        self.branch = branch
        self.remote = remote
        self.author_name = author_name.strip()
        self.author_email = author_email.strip()

    @staticmethod
    def _run(workspace: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=workspace,
            check=check,
            capture_output=True,
            text=True,
            timeout=120,
        )

    def _changed_files(self, workspace: Path) -> list[str]:
        output = self._run(
            workspace, "status", "--porcelain=v1", "-z", "--untracked-files=all"
        ).stdout
        files: list[str] = []
        for record in output.split("\0"):
            if not record:
                continue
            if len(record) < 4 or record[2] != " " or "R" in record[:2] or "C" in record[:2]:
                raise ValueError("could not safely parse publication changes")
            files.append(PurePosixPath(record[3:]).as_posix())
        return sorted(files)

    def create_candidate(
        self,
        workspace: Path,
        validated_files: list[str],
        message: str,
    ) -> str:
        workspace = workspace.resolve()
        expected = sorted(validated_files)
        if not expected or len(expected) != len(set(expected)):
            raise ValueError("validated publication file list is empty or duplicated")
        if self._changed_files(workspace) != expected:
            raise ValueError("validated files do not exactly match workspace changes")
        self._run(workspace, "add", "--", *expected)
        staged = self._run(
            workspace, "diff", "--cached", "--name-only", "-z", "--diff-filter=ACDMRTUXB"
        ).stdout
        if sorted(item for item in staged.split("\0") if item) != expected:
            raise ValueError("Git staged a file outside the validated publication set")
        self._run(
            workspace,
            "-c",
            f"user.name={self.author_name}",
            "-c",
            f"user.email={self.author_email}",
            "commit",
            "--no-gpg-sign",
            "-m",
            message[:500],
        )
        candidate = self._run(workspace, "rev-parse", "HEAD").stdout.strip()
        if not re.fullmatch(r"[0-9a-f]{40}", candidate):
            raise RuntimeError("candidate commit did not resolve to a full SHA")
        return candidate

    def is_published(self, workspace: Path, candidate_sha: str) -> bool:
        if not re.fullmatch(r"[0-9a-f]{40}", candidate_sha):
            raise ValueError("candidate SHA must be a full Git SHA")
        fetched = self._run(
            workspace,
            "fetch",
            "--no-tags",
            self.remote,
            f"+refs/heads/{self.branch}:refs/remotes/{self.remote}/{self.branch}",
            check=False,
        )
        if fetched.returncode != 0:
            raise RuntimeError(f"could not fetch publication branch: {fetched.stderr[-1000:]}")
        contains = self._run(
            workspace,
            "merge-base",
            "--is-ancestor",
            candidate_sha,
            f"refs/remotes/{self.remote}/{self.branch}",
            check=False,
        )
        if contains.returncode not in (0, 1):
            raise RuntimeError("could not reconcile candidate against publication branch")
        return contains.returncode == 0

    def publish(self, workspace: Path, candidate_sha: str) -> None:
        if self.is_published(workspace, candidate_sha):
            return
        pushed = self._run(
            workspace,
            "push",
            self.remote,
            f"{candidate_sha}:refs/heads/{self.branch}",
            check=False,
        )
        if pushed.returncode != 0:
            raise RuntimeError(f"Git publication failed: {pushed.stderr[-1000:]}")
        if not self.is_published(workspace, candidate_sha):
            raise RuntimeError("candidate is not reachable from the authoritative branch after push")
