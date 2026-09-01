from __future__ import annotations

import fcntl
import json
import os
import signal
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from pydantic import ValidationError

from spider_executor.artifacts import LocalArtifactStore
from spider_executor.failure import classify_runner_failure
from spider_executor.models import FailureClass, RunnerResult, ScrapedRecord


class SpiderRunner:
    def __init__(
        self,
        scripts_root: Path,
        artifacts: LocalArtifactStore,
        *,
        python_executable: str = sys.executable,
        timeout_seconds: int = 90,
        max_output_bytes: int = 1024 * 1024,
        memory_limit_bytes: int = 512 * 1024 * 1024,
        runtime_lock_path: Path | None = None,
    ) -> None:
        self.scripts_root = scripts_root.resolve()
        self.artifacts = artifacts
        self.python_executable = python_executable
        self.timeout_seconds = timeout_seconds
        self.max_output_bytes = max_output_bytes
        self.memory_limit_bytes = memory_limit_bytes
        self.runtime_lock_path = runtime_lock_path.resolve() if runtime_lock_path else None

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-c", f"safe.directory={self.scripts_root}", *args],
            cwd=self.scripts_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    def _failure(
        self,
        entry_id: str,
        run_id: str,
        failure: FailureClass,
        message: str,
        *,
        release: str | None = None,
        exit_code: int = 2,
        stderr: str = "",
    ) -> RunnerResult:
        record = ScrapedRecord(entry_id=entry_id, website=None, fields={}, errors=[message])
        content = json.dumps(record.model_dump(mode="json"), indent=2).encode()
        artifact = self.artifacts.put(f"runs/{run_id}/output.json", content)
        return RunnerResult(
            exit_code=exit_code,
            record=record,
            output_artifact=artifact,
            stderr=stderr or message,
            scraper_release=release,
            failure_class=failure,
        )

    def run(self, entry_id: str, run_id: str) -> RunnerResult:
        if self.runtime_lock_path is None:
            return self._run_unlocked(entry_id, run_id)
        self.runtime_lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.runtime_lock_path.open("a+") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_SH)
            return self._run_unlocked(entry_id, run_id)

    def _run_unlocked(self, entry_id: str, run_id: str) -> RunnerResult:
        try:
            release_process = self._git("rev-parse", "--verify", "HEAD^{commit}")
            dirty_process = self._git("status", "--porcelain", "--untracked-files=all")
        except (OSError, subprocess.SubprocessError) as exc:
            return self._failure(entry_id, run_id, FailureClass.OUTPUT_SCHEMA_FAILURE, f"Git metadata unavailable: {exc}")
        if release_process.returncode != 0:
            return self._failure(entry_id, run_id, FailureClass.OUTPUT_SCHEMA_FAILURE, "Git commit metadata unavailable")
        release = release_process.stdout.strip()
        if dirty_process.returncode != 0 or dirty_process.stdout.strip():
            return self._failure(
                entry_id,
                run_id,
                FailureClass.OUTPUT_SCHEMA_FAILURE,
                "spider-scripts checkout is dirty or unreadable",
                release=release,
            )

        with TemporaryDirectory(prefix="spider-run-") as temporary:
            stdout_path = Path(temporary) / "stdout"
            stderr_path = Path(temporary) / "stderr"
            with stdout_path.open("wb") as stdout_handle, stderr_path.open("wb") as stderr_handle:
                process: subprocess.Popen[bytes] | None = None
                try:
                    process = subprocess.Popen(
                        [
                            self.python_executable,
                            "-m",
                            "spider_executor.sandbox_exec",
                            str(self.max_output_bytes),
                            str(self.memory_limit_bytes),
                            str(max(1, int(self.timeout_seconds) + 1)),
                            self.python_executable,
                            "-m",
                            "core.run",
                            # single-token form: a separate value starting
                            # with "-" can be misread as an option flag
                            f"--entry-id={entry_id}",
                        ],
                        cwd=self.scripts_root,
                        stdout=stdout_handle,
                        stderr=stderr_handle,
                        env={
                            "PATH": os.environ.get("PATH", ""),
                            "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
                            "LANG": "C.UTF-8",
                            "PYTHONDONTWRITEBYTECODE": "1",
                        },
                        start_new_session=True,
                    )
                    process.wait(timeout=self.timeout_seconds)
                    exit_code = process.returncode
                except subprocess.TimeoutExpired:
                    if process is not None:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                    return self._failure(
                        entry_id,
                        run_id,
                        FailureClass.SANDBOX_TIMEOUT,
                        f"scraper timed out after {self.timeout_seconds} seconds",
                        release=release,
                        exit_code=124,
                    )
                except OSError as exc:
                    return self._failure(
                        entry_id,
                        run_id,
                        FailureClass.UNKNOWN,
                        f"scraper process could not start: {exc}",
                        release=release,
                    )
                finally:
                    if process is not None and process.poll() is not None:
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
            stdout = stdout_path.read_bytes()
            stderr_bytes = stderr_path.read_bytes()

        try:
            release_after = self._git("rev-parse", "--verify", "HEAD^{commit}")
            dirty_after = self._git("status", "--porcelain", "--untracked-files=all")
        except (OSError, subprocess.SubprocessError) as exc:
            return self._failure(
                entry_id,
                run_id,
                FailureClass.OUTPUT_SCHEMA_FAILURE,
                f"Git metadata unavailable after execution: {exc}",
                release=release,
            )
        if (
            release_after.returncode != 0
            or release_after.stdout.strip() != release
            or dirty_after.returncode != 0
            or dirty_after.stdout.strip()
        ):
            return self._failure(
                entry_id,
                run_id,
                FailureClass.OUTPUT_SCHEMA_FAILURE,
                "spider-scripts checkout changed during execution",
                release=release,
            )

        if len(stdout) >= self.max_output_bytes or len(stderr_bytes) >= self.max_output_bytes:
            return self._failure(
                entry_id,
                run_id,
                FailureClass.OUTPUT_SCHEMA_FAILURE,
                "scraper output exceeded configured limit",
                release=release,
            )
        stdout_text = stdout.decode("utf-8", errors="replace")
        stderr_text = stderr_bytes.decode("utf-8", errors="replace")
        try:
            record = ScrapedRecord.model_validate(json.loads(stdout_text))
        except (json.JSONDecodeError, ValidationError) as exc:
            return self._failure(
                entry_id,
                run_id,
                FailureClass.OUTPUT_SCHEMA_FAILURE,
                f"invalid runner output: {exc}",
                release=release,
                stderr=stderr_text,
            )

        content = json.dumps(record.model_dump(mode="json"), indent=2).encode()
        artifact = self.artifacts.put(f"runs/{run_id}/output.json", content)
        failure = None
        if exit_code != 0:
            failure = classify_runner_failure("\n".join(record.errors) or stderr_text)
        return RunnerResult(
            exit_code=exit_code,
            record=record,
            output_artifact=artifact,
            stderr=stderr_text,
            scraper_release=release,
            failure_class=failure,
        )
