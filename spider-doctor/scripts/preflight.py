#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIGEST = re.compile(r"^[A-Za-z0-9._/-]+@sha256:[0-9a-f]{64}$")


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"invalid environment line: {raw!r}")
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=False, capture_output=True, text=True, timeout=120)


def main() -> int:
    failures: list[str] = []
    env_file = ROOT / ".env"
    if not env_file.is_file():
        print("FAIL: .env is missing; copy .env.example and set reviewed values", file=sys.stderr)
        return 1

    try:
        configured = load_env(env_file)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    env = {**os.environ, **configured}

    image = env.get("SPIDER_DOCTOR_HERMES_IMAGE", "")
    if not DIGEST.fullmatch(image):
        failures.append("SPIDER_DOCTOR_HERMES_IMAGE is not pinned by a full sha256 digest")

    host_root = Path(env.get("SPIDER_DOCTOR_HOST_ROOT", ""))
    scripts_root = Path(env.get("SPIDER_SCRIPTS_HOST_PATH", ""))
    if host_root != ROOT:
        failures.append(f"SPIDER_DOCTOR_HOST_ROOT must be {ROOT}")
    if not (scripts_root / ".git").is_dir():
        failures.append("SPIDER_SCRIPTS_HOST_PATH is not a Git checkout")
    elif run("git", "-C", str(scripts_root), "status", "--porcelain").stdout.strip():
        failures.append("spider-scripts checkout is dirty")

    socket = Path("/var/run/docker.sock")
    if not socket.exists() or not stat.S_ISSOCK(socket.stat().st_mode):
        failures.append("Docker socket is unavailable")

    token = ROOT / "data" / "proxy-token"
    if not token.is_file() or token.stat().st_size == 0:
        failures.append("data/proxy-token is missing or empty")
    elif stat.S_IMODE(token.stat().st_mode) != 0o600:
        failures.append("data/proxy-token must have mode 0600")

    broker_auth = ROOT / "data" / "broker-hermes" / "auth.json"
    if not broker_auth.is_file() or broker_auth.stat().st_size == 0:
        failures.append("trusted broker OAuth is missing; run scripts/configure-hermes.sh")
    task_home = ROOT / "data" / "hermes"
    if not (task_home / "config.yaml").is_file():
        failures.append("credential-free task Hermes config is missing")
    for credential in (task_home / "auth.json", task_home / ".env"):
        if credential.exists() and credential.stat().st_size:
            failures.append(f"credential material is forbidden in task home: {credential}")

    task_network = env.get("SPIDER_DOCTOR_NETWORK", "spider-doctor-egress")
    policy = run(
        "docker", "network", "inspect", task_network,
        "--format", '{{ .Internal }}|{{ index .Labels "spider-doctor.egress-policy" }}',
    )
    if policy.returncode != 0 or policy.stdout.strip() != "true|restricted-v1":
        failures.append(
            "task network must be internal and carry the restricted-v1 policy label"
        )

    executor_network = env.get("SPIDER_EXECUTOR_CONTROL_NETWORK", "spider-executor_control")
    if run("docker", "network", "inspect", executor_network).returncode != 0:
        failures.append(f"executor control network is unavailable: {executor_network}")

    compose = subprocess.run(
        ["docker", "compose", "config", "--quiet"],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if compose.returncode != 0:
        failures.append(f"Docker Compose configuration is invalid: {compose.stderr.strip()}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print("PASS: Doctor deployment preflight succeeded")
    print("PASS: disposable tasks have no direct route; public HTTP(S) uses the restricted proxy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
