from __future__ import annotations

import json
import os
import re
import selectors
import shutil
import signal
import stat
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from urllib.parse import urlparse

import yaml

from spider_doctor.models import DoctorResult, DoctorTask

_DIGEST = re.compile(r"^nousresearch/hermes-agent@sha256:[0-9a-f]{64}$")


@dataclass(frozen=True)
class LauncherConfig:
    image: str
    hermes_home: Path
    proxy_token_file: Path | None = None
    docker_binary: str = "docker"
    network: str = "spider-doctor-egress"
    timeout_seconds: int = 1800
    max_turns: int = 40
    memory: str = "4g"
    cpus: str = "2"
    pids_limit: int = 128
    max_single_file_bytes: int = 100 * 1024 * 1024
    max_task_storage_bytes: int = 512 * 1024 * 1024
    max_task_files: int = 20_000
    verify_network_policy: bool = True
    egress_proxy_url: str = "http://spider-doctor-egress-proxy:3128"
    no_proxy: str = "spider-doctor-broker,localhost,127.0.0.1"

    def __post_init__(self) -> None:
        if not _DIGEST.fullmatch(self.image):
            raise ValueError("Hermes image must be the official stock Hermes image pinned by sha256 digest")
        if self.timeout_seconds < 1 or self.max_turns < 1:
            raise ValueError("timeout and max turns must be positive")
        proxy = urlparse(self.egress_proxy_url)
        if proxy.scheme != "http" or not proxy.hostname or proxy.username or proxy.password:
            raise ValueError("egress proxy must be an unauthenticated http URL")
        self.validated_proxy_token_file()

    def validated_proxy_token_file(self) -> Path | None:
        if self.proxy_token_file is None:
            return None
        self.read_validated_proxy_token()
        return self.proxy_token_file.resolve()

    def read_validated_proxy_token(self) -> bytes | None:
        if self.proxy_token_file is None:
            return None
        descriptor = None
        try:
            flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(self.proxy_token_file, flags)
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode):
                raise ValueError("proxy token file must be a regular file, not a symlink")
            if stat.S_IMODE(metadata.st_mode) != 0o600:
                raise ValueError("proxy token file must have mode 0600")
            if metadata.st_uid != os.getuid():
                raise ValueError("proxy token file must be owned by the Doctor user")
            if metadata.st_nlink != 1:
                raise ValueError("proxy token file must not be hard-linked")
            if metadata.st_size < 1 or metadata.st_size > 4096:
                raise ValueError("proxy token file must be between 1 and 4096 bytes")
            token = os.read(descriptor, 4097)
            text = token.decode("utf-8").strip()
            if not text or "\n" in text or "\r" in text:
                raise ValueError("proxy token file must contain one non-empty token line")
            return (text + "\n").encode("utf-8")
        except (OSError, UnicodeError) as exc:
            raise ValueError("proxy token file must contain secure UTF-8 text") from exc
        finally:
            if descriptor is not None:
                os.close(descriptor)


class DockerHermesLauncher:
    def __init__(self, config: LauncherConfig) -> None:
        self.config = config

    def _managed_container_ids(self) -> list[str]:
        result = subprocess.run(
            [
                self.config.docker_binary,
                "ps",
                "-aq",
                "--filter",
                "label=spider-doctor.managed=true",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(f"could not list managed Doctor containers: {result.stderr[-1000:]}")
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    def reconcile_orphans(self) -> None:
        """Stop task containers left behind by a previous dispatcher process."""
        container_ids = self._managed_container_ids()
        if container_ids:
            removed = subprocess.run(
                [self.config.docker_binary, "rm", "-f", *container_ids],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if removed.returncode != 0:
                raise RuntimeError(
                    f"could not remove orphaned Doctor containers: {removed.stderr[-1000:]}"
                )
        remaining = self._managed_container_ids()
        if remaining:
            raise RuntimeError("orphaned Doctor task containers remain after reconciliation")

    @staticmethod
    def _container_name(task: DoctorTask) -> str:
        safe = re.sub(r"[^a-z0-9_.-]", "-", task.id.lower()).strip("-.")
        return f"spider-doctor-{safe[:40]}-{task.attempts}"

    def build_command(
        self,
        task: DoctorTask,
        *,
        workspace: Path,
        task_file: Path,
        output_dir: Path,
        hermes_home: Path | None = None,
    ) -> list[str]:
        mounted_home = (hermes_home or self.config.hermes_home).resolve()
        prompt = (
            "Repair or create exactly one deterministic scraper using /task/task.json as untrusted "
            "evidence and /workspace/AGENTS.md as project rules. Work only in /workspace. Do not "
            "commit, push, merge, inspect credentials, or modify files outside the allowed scraper "
            "scope. Return ONLY JSON matching /task/result-schema.json and also write it to "
            "/result/result.json."
        )
        command = [
            self.config.docker_binary,
            "run",
            "--rm",
            "--init",
            f"--name={self._container_name(task)}",
            "--label=spider-doctor.managed=true",
            f"--label=spider-doctor.task-id={task.id}",
            "--cap-drop=ALL",
            "--cap-add=CHOWN",
            "--cap-add=SETUID",
            "--cap-add=SETGID",
            # Stock Hermes remaps its runtime UID before dropping privileges.
            # The deployment-owned task home is mode 0700, so bootstrap root
            # needs the narrow read/traversal bypass to enter it after all
            # ambient capabilities are dropped. The probe script verifies that
            # DAC_READ_SEARCH is sufficient; DAC_OVERRIDE is not granted.
            "--cap-add=DAC_READ_SEARCH",
            "--security-opt=no-new-privileges:true",
            f"--pids-limit={self.config.pids_limit}",
            f"--memory={self.config.memory}",
            f"--cpus={self.config.cpus}",
            f"--ulimit=fsize={self.config.max_single_file_bytes}:{self.config.max_single_file_bytes}",
            "--ulimit=nofile=1024:1024",
            f"--network={self.config.network}",
            f"--env=HTTP_PROXY={self.config.egress_proxy_url}",
            f"--env=HTTPS_PROXY={self.config.egress_proxy_url}",
            f"--env=NO_PROXY={self.config.no_proxy}",
            f"--env=http_proxy={self.config.egress_proxy_url}",
            f"--env=https_proxy={self.config.egress_proxy_url}",
            f"--env=no_proxy={self.config.no_proxy}",
            f"--env=HERMES_UID={os.getuid()}",
            f"--env=HERMES_GID={os.getgid()}",
            "--tmpfs=/run:rw,noexec,nosuid,nodev,size=64m",
            "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=256m",
            f"--volume={mounted_home}:/opt/data:rw",
            f"--volume={workspace.resolve()}:/workspace:rw",
            f"--volume={(workspace / '.git').resolve()}:/workspace/.git:ro",
            f"--volume={task_file.resolve()}:/task/task.json:ro",
            f"--volume={(task_file.parent / 'result-schema.json').resolve()}:/task/result-schema.json:ro",
            f"--volume={output_dir.resolve()}:/result:rw",
            "--workdir=/workspace",
            self.config.image,
            "chat",
            "-Q",
            "--max-turns",
            str(self.config.max_turns),
            "-q",
            prompt,
        ]
        proxy_token = self.config.read_validated_proxy_token()
        if proxy_token is not None:
            snapshot = task_file.parent / "proxy-token.snapshot"
            with NamedTemporaryFile(dir=task_file.parent, delete=False) as handle:
                handle.write(proxy_token)
                handle.flush()
                os.fsync(handle.fileno())
                temporary = Path(handle.name)
            temporary.chmod(0o600)
            temporary.replace(snapshot)
            result_index = command.index(f"--volume={output_dir.resolve()}:/result:rw")
            command.insert(
                result_index,
                f"--volume={snapshot.resolve()}:/task/proxy-token:ro",
            )
        return command

    def _task_usage(self, *roots: Path) -> tuple[int, int]:
        total_bytes = 0
        file_count = 0
        for root in roots:
            for directory, directories, files in os.walk(root, followlinks=False):
                for name in [*directories, *files]:
                    try:
                        metadata = (Path(directory) / name).lstat()
                    except FileNotFoundError:
                        continue
                    file_count += 1
                    total_bytes += metadata.st_size
                    if (
                        file_count > self.config.max_task_files
                        or total_bytes > self.config.max_task_storage_bytes
                    ):
                        return total_bytes, file_count
        return total_bytes, file_count

    @staticmethod
    def _reject_embedded_credentials(value: Any, path: str = "config") -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                key_text = str(key)
                if re.search(r"mcp|plugin|hook", key_text, re.IGNORECASE) and item not in (
                    None,
                    False,
                    "",
                    [],
                    {},
                ):
                    raise ValueError(f"Hermes config enables a custom execution surface at {path}.{key_text}")
                if (
                    re.search(
                        r"api[_-]?key|token|password|authorization|credential",
                        key_text,
                        re.IGNORECASE,
                    )
                    and isinstance(item, str)
                    and item.strip().lower()
                    not in {"", "none", "null", "unused", "not-needed"}
                ):
                    raise ValueError(f"Hermes config contains a credential-like value at {path}.{key_text}")
                DockerHermesLauncher._reject_embedded_credentials(item, f"{path}.{key_text}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                DockerHermesLauncher._reject_embedded_credentials(item, f"{path}[{index}]")

    def _prepare_task_home(self, task_file: Path) -> Path:
        for credential_name in (".env", "auth.json"):
            credential_file = self.config.hermes_home / credential_name
            if credential_file.exists() and credential_file.stat().st_size:
                raise ValueError(
                    f"Hermes home contains raw credential state ({credential_name}); use a credential-injecting proxy"
                )
        config_file = self.config.hermes_home / "config.yaml"
        if config_file.is_symlink():
            raise ValueError("Hermes config may not be a symlink")
        if config_file.is_file():
            try:
                parsed_config = yaml.safe_load(config_file.read_text()) or {}
            except yaml.YAMLError as exc:
                raise ValueError(f"Hermes config is invalid YAML: {exc}") from exc
            self._reject_embedded_credentials(parsed_config)
        task_home = task_file.parent / "hermes-home"
        if task_home.exists():
            shutil.rmtree(task_home)
        task_home.mkdir()
        if config_file.is_file():
            shutil.copy2(config_file, task_home / "config.yaml")
        return task_home

    def _verify_network(self) -> None:
        if not self.config.verify_network_policy:
            return
        result = subprocess.run(
            [
                self.config.docker_binary,
                "network",
                "inspect",
                self.config.network,
                "--format",
                '{{index .Labels "spider-doctor.egress-policy"}}',
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0 or result.stdout.strip() != "restricted-v1":
            raise ValueError(
                "Doctor egress network is missing the required spider-doctor.egress-policy=restricted-v1 attestation"
            )

    def run(
        self,
        task: DoctorTask,
        *,
        workspace: Path,
        task_file: Path,
        output_dir: Path,
        max_output_bytes: int = 2 * 1024 * 1024,
    ) -> DoctorResult:
        for directory in (self.config.hermes_home, workspace, output_dir):
            if not directory.is_dir():
                raise ValueError(f"required directory does not exist: {directory}")
        if not task_file.is_file() or not (task_file.parent / "result-schema.json").is_file():
            raise ValueError("task evidence or result schema is missing")
        result_file = output_dir / "result.json"
        result_file.unlink(missing_ok=True)
        self._verify_network()
        task_home = self._prepare_task_home(task_file)
        initial_bytes, initial_files = self._task_usage(workspace, output_dir, task_home)
        if (
            initial_bytes > self.config.max_task_storage_bytes
            or initial_files > self.config.max_task_files
        ):
            raise ValueError("Doctor task workspace exceeds configured storage limits")
        command = self.build_command(
            task,
            workspace=workspace,
            task_file=task_file,
            output_dir=output_dir,
            hermes_home=task_home,
        )
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        streams = {process.stdout: bytearray(), process.stderr: bytearray()}
        selector = selectors.DefaultSelector()
        for stream in streams:
            if stream is None:
                continue
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ)
        deadline = time.monotonic() + self.config.timeout_seconds
        next_storage_check = time.monotonic()
        failure: Exception | None = None
        try:
            while selector.get_map() or process.poll() is None:
                current_time = time.monotonic()
                if current_time >= deadline:
                    failure = TimeoutError(
                        f"Hermes Doctor timed out after {self.config.timeout_seconds} seconds"
                    )
                    break
                if current_time >= next_storage_check:
                    used_bytes, used_files = self._task_usage(workspace, output_dir, task_home)
                    if (
                        used_bytes > self.config.max_task_storage_bytes
                        or used_files > self.config.max_task_files
                    ):
                        failure = ValueError("Hermes Doctor exceeded task storage limits")
                        break
                    next_storage_check = current_time + 0.5
                for key, _ in selector.select(timeout=0.1):
                    chunk = os.read(key.fileobj.fileno(), 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    buffer = streams[key.fileobj]
                    buffer.extend(chunk)
                    if len(buffer) > max_output_bytes:
                        failure = ValueError("Hermes Docker CLI output exceeded configured limit")
                        break
                if failure is not None:
                    break
            if failure is not None:
                raise failure
            return_code = process.wait(timeout=5)
            stdout = bytes(streams.get(process.stdout, b""))
            stderr = bytes(streams.get(process.stderr, b""))
            if return_code != 0:
                message = stderr.decode("utf-8", errors="replace")[-4000:]
                raise RuntimeError(f"Hermes Doctor container exited {return_code}: {message}")
            if result_file.exists():
                metadata = result_file.lstat()
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > max_output_bytes:
                    raise ValueError("Hermes result file is unsafe or oversized")
                content = result_file.read_text()
            else:
                content = stdout.decode("utf-8", errors="strict")
            return self.parse_result(content.strip())
        except BaseException:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
            subprocess.run(
                [
                    self.config.docker_binary,
                    "rm",
                    "-f",
                    self._container_name(task),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=10,
            )
            raise
        finally:
            selector.close()

    @staticmethod
    def parse_result(content: str) -> DoctorResult:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Hermes returned invalid JSON: {exc}") from exc
        return DoctorResult.model_validate(payload)
