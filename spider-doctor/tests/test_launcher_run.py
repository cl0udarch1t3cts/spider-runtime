from pathlib import Path

import pytest
from test_launcher import DIGEST, task

from spider_doctor.launcher import DockerHermesLauncher, LauncherConfig
from spider_doctor.models import DoctorStatus


def make_inputs(tmp_path: Path):
    home = tmp_path / "home"
    workspace = tmp_path / "workspace"
    task_dir = tmp_path / "task"
    output = tmp_path / "output"
    for path in (home, workspace, task_dir, output):
        path.mkdir()
    task_file = task_dir / "task.json"
    task_file.write_text("{}")
    (task_dir / "result-schema.json").write_text("{}")
    return home, workspace, task_file, output


def executable(tmp_path: Path, body: str) -> Path:
    script = tmp_path / "fake-docker"
    script.write_text("#!/usr/bin/env python3\n" + body)
    script.chmod(0o755)
    return script


def test_run_parses_bounded_oneshot_json(tmp_path: Path) -> None:
    home, workspace, task_file, output = make_inputs(tmp_path)
    fake = executable(
        tmp_path,
        "import json\nprint(json.dumps({'status':'awaiting_review','summary':'fixed','changed_files':[],'tests':['pytest'],'errors':[]}))\n",
    )
    launcher = DockerHermesLauncher(
        LauncherConfig(
            image=DIGEST,
            hermes_home=home,
            docker_binary=str(fake),
            timeout_seconds=5,
            verify_network_policy=False,
        )
    )

    result = launcher.run(task(), workspace=workspace, task_file=task_file, output_dir=output)

    assert result.status == DoctorStatus.AWAITING_REVIEW
    assert result.summary == "fixed"


def test_run_kills_timed_out_cli_and_fails_closed(tmp_path: Path) -> None:
    home, workspace, task_file, output = make_inputs(tmp_path)
    fake = executable(
        tmp_path,
        "import sys, time\n"
        "if len(sys.argv) > 1 and sys.argv[1] == 'rm': raise SystemExit(0)\n"
        "time.sleep(30)\n",
    )
    launcher = DockerHermesLauncher(
        LauncherConfig(
            image=DIGEST,
            hermes_home=home,
            docker_binary=str(fake),
            timeout_seconds=1,
            verify_network_policy=False,
        )
    )

    with pytest.raises(TimeoutError, match="timed out"):
        launcher.run(task(), workspace=workspace, task_file=task_file, output_dir=output)


def test_run_uses_disposable_hermes_home_not_seed_volume(tmp_path: Path) -> None:
    home, workspace, task_file, output = make_inputs(tmp_path)
    (home / "config.yaml").write_text("model: {}\n")
    argv_file = tmp_path / "argv.json"
    fake = executable(
        tmp_path,
        "import json, sys\n"
        f"open({str(argv_file)!r}, 'w').write(json.dumps(sys.argv))\n"
        "print(json.dumps({'status':'failed','summary':'no patch','changed_files':[],'tests':[],'errors':['expected']}))\n",
    )
    launcher = DockerHermesLauncher(
        LauncherConfig(
            image=DIGEST,
            hermes_home=home,
            docker_binary=str(fake),
            timeout_seconds=5,
            verify_network_policy=False,
        )
    )

    launcher.run(task(), workspace=workspace, task_file=task_file, output_dir=output)

    arguments = argv_file.read_text()
    assert f"{home.resolve()}:/opt/data:rw" not in arguments
    assert f"{task_file.parent.resolve()}/hermes-home:/opt/data:rw" in arguments
    assert (task_file.parent / "hermes-home" / "config.yaml").is_file()


def test_run_accepts_scoped_broker_key_command(tmp_path: Path) -> None:
    home, workspace, task_file, output = make_inputs(tmp_path)
    (home / "config.yaml").write_text(
        "providers:\n"
        "  doctor-codex:\n"
        "    api: http://172.30.0.1:8645/v1\n"
        "    transport: codex_responses\n"
        "    key_cmd: cat /task/proxy-token\n"
        "model:\n"
        "  provider: custom:doctor-codex\n"
        "  default: gpt-5.4\n"
    )
    token_file = tmp_path / "proxy-token"
    token_file.write_text("scoped-broker-token\n")
    token_file.chmod(0o600)
    fake = executable(
        tmp_path,
        "import json\n"
        "print(json.dumps({'status':'failed','summary':'expected','changed_files':[],"
        "'tests':[],'errors':['expected']}))\n",
    )
    launcher = DockerHermesLauncher(
        LauncherConfig(
            image=DIGEST,
            hermes_home=home,
            proxy_token_file=token_file,
            docker_binary=str(fake),
            timeout_seconds=5,
            verify_network_policy=False,
        )
    )

    result = launcher.run(task(), workspace=workspace, task_file=task_file, output_dir=output)

    assert result.status == DoctorStatus.FAILED
    assert (task_file.parent / "hermes-home" / "config.yaml").is_file()


def test_run_rejects_raw_provider_credentials_in_seed_home(tmp_path: Path) -> None:
    home, workspace, task_file, output = make_inputs(tmp_path)
    (home / ".env").write_text("OPENAI_API_KEY=secret\n")
    fake = executable(tmp_path, "raise SystemExit(0)\n")
    launcher = DockerHermesLauncher(
        LauncherConfig(
            image=DIGEST,
            hermes_home=home,
            docker_binary=str(fake),
            timeout_seconds=5,
            verify_network_policy=False,
        )
    )

    with pytest.raises(ValueError, match="raw credential"):
        launcher.run(task(), workspace=workspace, task_file=task_file, output_dir=output)


def test_run_rejects_secret_embedded_in_config_yaml(tmp_path: Path) -> None:
    home, workspace, task_file, output = make_inputs(tmp_path)
    (home / "config.yaml").write_text("model:\n  api_key: sk-secret\n")
    fake = executable(tmp_path, "raise SystemExit(0)\n")
    launcher = DockerHermesLauncher(
        LauncherConfig(
            image=DIGEST,
            hermes_home=home,
            docker_binary=str(fake),
            timeout_seconds=5,
            verify_network_policy=False,
        )
    )

    with pytest.raises(ValueError, match="credential-like"):
        launcher.run(task(), workspace=workspace, task_file=task_file, output_dir=output)


def test_network_requires_restricted_policy_attestation(tmp_path: Path) -> None:
    home, _, _, _ = make_inputs(tmp_path)
    fake = executable(tmp_path, "print('unrestricted')\n")
    launcher = DockerHermesLauncher(
        LauncherConfig(image=DIGEST, hermes_home=home, docker_binary=str(fake))
    )

    with pytest.raises(ValueError, match="egress-policy=restricted-v1"):
        launcher._verify_network()


def test_task_usage_counts_directories_and_directory_symlinks(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir()
    root = tmp_path / "tree"
    root.mkdir()
    for index in range(12):
        (root / f"directory-{index}").mkdir()
    (root / "directory-link").symlink_to(root / "directory-0", target_is_directory=True)
    launcher = DockerHermesLauncher(
        LauncherConfig(
            image=DIGEST,
            hermes_home=home,
            max_task_files=10,
            verify_network_policy=False,
        )
    )

    _, entries = launcher._task_usage(root)

    assert entries > 10


def test_run_writes_model_override_into_the_task_home_config(tmp_path: Path) -> None:
    import yaml

    home, workspace, task_file, output = make_inputs(tmp_path)
    (home / "config.yaml").write_text(
        "model:\n  default: gpt-5.4\n  provider: custom:doctor-codex\n"
        "providers:\n  doctor-codex:\n    api: http://spider-doctor-broker:8645/v1\n"
    )
    fake = executable(
        tmp_path,
        "import json\nprint(json.dumps({'status':'awaiting_review','summary':'ok','changed_files':[],'tests':[],'errors':[]}))\n",
    )
    launcher = DockerHermesLauncher(
        LauncherConfig(
            image=DIGEST,
            hermes_home=home,
            docker_binary=str(fake),
            timeout_seconds=5,
            verify_network_policy=False,
        )
    )

    launcher.run(
        task(),
        workspace=workspace,
        task_file=task_file,
        output_dir=output,
        model="qwen3-coder:free",
        provider="doctor-openrouter",
    )

    task_config = yaml.safe_load((task_file.parent / "hermes-home" / "config.yaml").read_text())
    assert task_config["model"]["default"] == "qwen3-coder:free"
    assert task_config["model"]["provider"] == "custom:doctor-openrouter"
    # The shared template must stay untouched.
    template = yaml.safe_load((home / "config.yaml").read_text())
    assert template["model"]["default"] == "gpt-5.4"


def test_run_without_model_override_copies_config_verbatim(tmp_path: Path) -> None:
    import yaml

    home, workspace, task_file, output = make_inputs(tmp_path)
    (home / "config.yaml").write_text("model:\n  default: gpt-5.4\n")
    fake = executable(
        tmp_path,
        "import json\nprint(json.dumps({'status':'awaiting_review','summary':'ok','changed_files':[],'tests':[],'errors':[]}))\n",
    )
    launcher = DockerHermesLauncher(
        LauncherConfig(
            image=DIGEST,
            hermes_home=home,
            docker_binary=str(fake),
            timeout_seconds=5,
            verify_network_policy=False,
        )
    )

    launcher.run(task(), workspace=workspace, task_file=task_file, output_dir=output)

    task_config = yaml.safe_load((task_file.parent / "hermes-home" / "config.yaml").read_text())
    assert task_config == {"model": {"default": "gpt-5.4"}}
