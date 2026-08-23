from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_compose_keeps_hermes_in_digest_pinned_containers() -> None:
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text())
    services = compose["services"]

    assert set(services) == {"broker", "doctor", "egress-proxy"}
    assert services["broker"]["build"]["dockerfile"] == "Dockerfile.broker"
    assert services["broker"]["build"]["args"]["HERMES_BASE_IMAGE"] == (
        "nousresearch/hermes-agent@${SPIDER_DOCTOR_HERMES_DIGEST:?set the reviewed stock Hermes digest}"
    )
    assert services["broker"]["entrypoint"] == [
        "/opt/hermes/.venv/bin/python",
        "/opt/spider-doctor/codex_broker.py",
    ]
    assert services["broker"]["user"] == "${SPIDER_DOCTOR_UID}:${SPIDER_DOCTOR_GID}"
    assert services["doctor"]["build"]["context"] == "."
    assert services["doctor"]["build"]["args"] == {
        "SPIDER_DOCTOR_UID": "${SPIDER_DOCTOR_UID}",
        "SPIDER_DOCTOR_GID": "${SPIDER_DOCTOR_GID}",
    }
    dockerfile = (ROOT / "Dockerfile").read_text()
    assert "ARG SPIDER_DOCTOR_UID" in dockerfile
    assert "ARG SPIDER_DOCTOR_GID" in dockerfile
    assert 'useradd --uid "$SPIDER_DOCTOR_UID"' in dockerfile
    assert services["doctor"]["environment"]["SPIDER_DOCTOR_HERMES_IMAGE"] == (
        "nousresearch/hermes-agent@${SPIDER_DOCTOR_HERMES_DIGEST}"
    )


def test_task_network_is_internal_and_egress_requires_proxy() -> None:
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text())
    squid = (ROOT / "deploy" / "squid.conf").read_text()

    task_network = compose["networks"]["task-egress"]
    assert task_network == {
        "name": "${SPIDER_DOCTOR_NETWORK:-spider-doctor-egress}",
        "internal": True,
        "labels": {"spider-doctor.egress-policy": "restricted-v1"},
    }
    assert compose["services"]["broker"]["networks"]["task-egress"]["aliases"] == [
        "spider-doctor-broker"
    ]
    proxy = compose["services"]["egress-proxy"]
    assert set(proxy["networks"]) == {"task-egress", "uplink"}
    assert proxy["networks"]["task-egress"]["aliases"] == [
        "spider-doctor-egress-proxy"
    ]
    assert "acl allowed_protocol proto HTTP HTTPS" in squid
    assert "http_access deny !allowed_protocol !CONNECT" in squid
    assert "acl blocked_v4 dst 169.254.0.0/16" in squid
    assert "acl blocked_v6 dst fc00::/7" in squid
    assert "acl blocked_names dstdomain localhost .local .internal" in squid
    assert ".localhost" not in squid
    assert "pinger_enable off" in squid


def test_dispatcher_mounts_only_required_daemon_paths_at_identical_host_paths() -> None:
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text())
    doctor = compose["services"]["doctor"]
    volumes = doctor["volumes"]

    assert "/var/run/docker.sock:/var/run/docker.sock" in volumes
    assert (
        "${SPIDER_DOCTOR_HOST_ROOT:?set the absolute Doctor checkout path}/data/workspaces:"
        "${SPIDER_DOCTOR_HOST_ROOT}/data/workspaces:rw"
    ) in volumes
    assert (
        "${SPIDER_DOCTOR_HOST_ROOT}/data/tasks:"
        "${SPIDER_DOCTOR_HOST_ROOT}/data/tasks:rw"
    ) in volumes
    assert (
        "${SPIDER_DOCTOR_HOST_ROOT}/data/hermes:"
        "${SPIDER_DOCTOR_HOST_ROOT}/data/hermes:ro"
    ) in volumes
    assert (
        "${SPIDER_SCRIPTS_HOST_PATH:?set the absolute spider-scripts path}:"
        "${SPIDER_SCRIPTS_HOST_PATH}:ro"
    ) in volumes
    assert not any("broker-hermes" in volume for volume in volumes)
    assert doctor["working_dir"] == "/opt/spider-doctor"


def test_example_environment_contains_settings_not_credentials() -> None:
    text = (ROOT / ".env.example").read_text()

    assert "SPIDER_DOCTOR_HERMES_DIGEST=sha256:" in text
    assert "SPIDER_DOCTOR_HOST_ROOT=/home/spider/projects/spider-runtime/spider-doctor" in text
    assert "SPIDER_SCRIPTS_HOST_PATH=/home/spider/projects/spider-scripts" in text
    assert "TOKEN=" not in text
    assert "PASSWORD=" not in text
    assert "AUTH=" not in text
    assert "nousresearch/hermes-agent@" not in text


def test_preflight_and_setup_require_official_stock_hermes() -> None:
    preflight = (ROOT / "scripts" / "preflight.py").read_text()
    setup = (ROOT / "scripts" / "configure-hermes.sh").read_text()

    assert 'r"^sha256:[0-9a-f]{64}$"' in preflight
    assert 'HERMES_IMAGE="nousresearch/hermes-agent@${SPIDER_DOCTOR_HERMES_DIGEST}"' in setup


def test_setup_script_uses_separate_trusted_and_credential_free_homes() -> None:
    init_env = (ROOT / "scripts" / "init-env.py").read_text()
    script = (ROOT / "scripts" / "configure-hermes.sh").read_text()

    assert "os.getuid()" in init_env
    assert 'Path("/var/run/docker.sock").stat().st_gid' in init_env
    assert "rm -f data/hermes/config.yaml data/hermes/config.yaml.bak-*" in script
    assert script.index("rm -f data/hermes/config.yaml") < script.index("run_task_hermes config set")
    assert 'data/broker-hermes:/opt/data' in script
    assert 'data/hermes:/opt/data' in script
    assert "auth add openai-codex" in script
    assert "http://spider-doctor-broker:8645/v1" in script
    assert "providers.doctor-codex.key_cmd" in script
    assert "cat /task/proxy-token" in script
    assert "rm -f data/hermes/.env" in script


def test_runtime_secrets_and_legacy_sandbox_are_ignored() -> None:
    ignored = set((ROOT / ".gitignore").read_text().splitlines())
    docker_ignored = set((ROOT / ".dockerignore").read_text().splitlines())

    assert ".env" in ignored
    assert "/data/" in ignored
    assert "/sandbox/" in ignored
    assert {".env", "data/", ".git/", "sandbox/"} <= docker_ignored


def test_start_fails_closed_through_preflight() -> None:
    preflight = (ROOT / "scripts" / "preflight.py").read_text()
    start = (ROOT / "scripts" / "start.sh").read_text()

    assert 'spider-doctor.egress-policy' in preflight
    assert 'restricted-v1' in preflight
    assert '"network", "inspect"' in preflight
    assert 'true|restricted-v1' in preflight
    assert "scripts/preflight.py" in start
    assert "docker compose up --build -d egress-proxy\npython3 scripts/preflight.py" in start
    assert "egress-proxy broker\npython3 scripts/preflight.py" not in start
    assert "docker compose up --build -d --wait" in start
