import os
import subprocess
from pathlib import Path

import pytest

from spider_doctor.launcher import DockerHermesLauncher, LauncherConfig
from spider_doctor.models import DoctorTask

DIGEST = "nousresearch/hermes-agent@sha256:" + "a" * 64


def task() -> DoctorTask:
    return DoctorTask.model_validate(
        {
            "_id": "task-1",
            "entry_id": "example",
            "type": "repair",
            "status": "running",
            "attempts": 1,
            "max_attempts": 2,
            "source_run_id": "job:1",
            "failure_class": "SCRAPER_EXCEPTION",
            "errors": ["boom"],
            "lease": {"worker_id": "doctor", "token": "lease", "expires_at": "2030-01-01T00:00:00Z"},
        }
    )


def test_launcher_rejects_mutable_image_reference(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="digest"):
        LauncherConfig(image="nousresearch/hermes-agent:latest", hermes_home=tmp_path)


def test_launcher_rejects_nonofficial_digest_pinned_image(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="official stock Hermes"):
        LauncherConfig(image="attacker/hermes-agent@sha256:" + "a" * 64, hermes_home=tmp_path)


def test_command_has_fail_closed_container_boundaries(tmp_path: Path) -> None:
    config = LauncherConfig(image=DIGEST, hermes_home=tmp_path / "hermes", timeout_seconds=600)
    launcher = DockerHermesLauncher(config)
    command = launcher.build_command(
        task(),
        workspace=tmp_path / "workspace",
        task_file=tmp_path / "task.json",
        output_dir=tmp_path / "output",
    )
    joined = " ".join(command)

    assert command[:4] == ["docker", "run", "--rm", "--init"]
    # The official image detects Docker's injected PID-1 init and uses its
    # supported direct-bootstrap path for this one-shot command. That avoids
    # starting the writable s6 supervision tree and keeps /run non-executable.
    assert "--read-only" not in command
    assert "--tmpfs=/run:rw,noexec,nosuid,nodev,size=64m" in command
    assert "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=512m" in command
    assert not any(value.startswith("--tmpfs=/run:") and ",exec," in value for value in command)
    assert not any(value.startswith("--tmpfs=/tmp:") and ",exec," in value for value in command)
    assert "--cap-drop=ALL" in command
    assert "--cap-add=CHOWN" in command
    assert "--cap-add=SETUID" in command
    assert "--cap-add=SETGID" in command
    assert "--cap-add=DAC_READ_SEARCH" in command
    assert not any(
        value.startswith("--cap-add=")
        and value
        not in {
            "--cap-add=CHOWN",
            "--cap-add=SETUID",
            "--cap-add=SETGID",
            "--cap-add=DAC_READ_SEARCH",
        }
        for value in command
    )
    assert "--security-opt=no-new-privileges:true" in command
    assert "--pids-limit=128" in command
    assert "--memory=4g" in command
    assert "--cpus=2" in command
    assert "--ulimit=fsize=104857600:104857600" in command
    assert "--ulimit=nofile=1024:1024" in command
    assert "--label=spider-doctor.managed=true" in command
    assert "--label=spider-doctor.task-id=task-1" in command
    assert "--env=HTTP_PROXY=http://spider-doctor-egress-proxy:3128" in command
    assert "--env=HTTPS_PROXY=http://spider-doctor-egress-proxy:3128" in command
    assert "--env=NO_PROXY=spider-doctor-broker,localhost,127.0.0.1" in command
    assert "--env=https_proxy=http://spider-doctor-egress-proxy:3128" in command
    assert "--env=no_proxy=spider-doctor-broker,localhost,127.0.0.1" in command
    assert f"--env=HERMES_UID={os.getuid()}" in command
    assert f"--env=HERMES_GID={os.getgid()}" in command
    assert "--env=UV_CACHE_DIR=/tmp/uv-cache" in command
    assert "--env=PIP_CACHE_DIR=/tmp/pip-cache" in command
    assert "--env=XDG_CACHE_HOME=/tmp/cache" in command
    assert ":/workspace:rw" in joined
    assert ":/workspace/.git:ro" in joined
    assert ":/task/task.json:ro" in joined
    assert ":/result:rw" in joined
    assert "/var/run/docker.sock" not in joined
    assert "MONGODB" not in joined.upper()
    assert command[-1].startswith("Repair or create exactly one deterministic scraper")


def test_command_mounts_scoped_broker_token_without_embedding_secret(tmp_path: Path) -> None:
    token_file = tmp_path / "proxy-token"
    token_file.write_text("scoped-broker-token\n")
    token_file.chmod(0o600)
    config = LauncherConfig(
        image=DIGEST,
        hermes_home=tmp_path / "hermes",
        proxy_token_file=token_file,
    )

    command = DockerHermesLauncher(config).build_command(
        task(),
        workspace=tmp_path / "workspace",
        task_file=tmp_path / "task.json",
        output_dir=tmp_path / "output",
    )

    snapshot = tmp_path / "proxy-token.snapshot"
    assert f"--volume={snapshot.resolve()}:/task/proxy-token:ro" in command
    assert snapshot.read_text() == "scoped-broker-token\n"
    assert "scoped-broker-token" not in " ".join(command)


def test_startup_reconciliation_force_removes_all_managed_task_containers(
    tmp_path: Path, monkeypatch
) -> None:
    calls = []
    ps_results = ["container-a\ncontainer-b\n", ""]

    def fake_run(argv, **kwargs):
        calls.append(argv)
        if argv[1:3] == ["ps", "-aq"]:
            return subprocess.CompletedProcess(argv, 0, stdout=ps_results.pop(0), stderr="")
        if argv[1:3] == ["rm", "-f"]:
            return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
        raise AssertionError(f"unexpected Docker command: {argv}")

    monkeypatch.setattr(subprocess, "run", fake_run)
    launcher = DockerHermesLauncher(LauncherConfig(image=DIGEST, hermes_home=tmp_path))

    launcher.reconcile_orphans()

    assert calls == [
        ["docker", "ps", "-aq", "--filter", "label=spider-doctor.managed=true"],
        ["docker", "rm", "-f", "container-a", "container-b"],
        ["docker", "ps", "-aq", "--filter", "label=spider-doctor.managed=true"],
    ]


def test_launcher_rejects_insecure_broker_token_file(tmp_path: Path) -> None:
    token_file = tmp_path / "proxy-token"
    token_file.write_text("scoped-broker-token\n")
    token_file.chmod(0o644)

    with pytest.raises(ValueError, match="0600"):
        LauncherConfig(
            image=DIGEST,
            hermes_home=tmp_path / "hermes",
            proxy_token_file=token_file,
        )


def test_launcher_revalidates_broker_token_before_each_container(tmp_path: Path) -> None:
    token_file = tmp_path / "proxy-token"
    token_file.write_text("scoped-broker-token\n")
    token_file.chmod(0o600)
    config = LauncherConfig(
        image=DIGEST,
        hermes_home=tmp_path / "hermes",
        proxy_token_file=token_file,
    )
    token_file.chmod(0o644)

    with pytest.raises(ValueError, match="0600"):
        DockerHermesLauncher(config).build_command(
            task(),
            workspace=tmp_path / "workspace",
            task_file=tmp_path / "task.json",
            output_dir=tmp_path / "output",
        )


def test_result_rejects_path_traversal(tmp_path: Path) -> None:
    launcher = DockerHermesLauncher(LauncherConfig(image=DIGEST, hermes_home=tmp_path))
    with pytest.raises(ValueError, match="unsafe changed file"):
        launcher.parse_result(
            '{"status":"awaiting_review","summary":"fixed","changed_files":["../secret"],"tests":[],"errors":[]}'
        )
