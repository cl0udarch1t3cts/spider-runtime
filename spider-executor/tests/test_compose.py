from pathlib import Path

from spider_executor.settings import Settings


ROOT = Path(__file__).resolve().parents[1]


def test_mongodb_is_published_only_on_host_loopback() -> None:
    compose = (ROOT / "docker-compose.yml").read_text()

    assert '      - "127.0.0.1:27017:27017"' in compose
    assert '      - "27017:27017"' not in compose
    assert '      - "0.0.0.0:27017:27017"' not in compose


def test_runtime_volumes_are_initialized_for_the_runtime_user() -> None:
    compose = (ROOT / "docker-compose.yml").read_text()

    assert "  runtime-init:\n" in compose
    assert "SPIDER_EXECUTOR_UID: ${SPIDER_EXECUTOR_UID:-1000}" in compose
    assert "SPIDER_EXECUTOR_GID: ${SPIDER_EXECUTOR_GID:-1000}" in compose
    assert '    user: "0:0"\n' in compose
    assert "    network_mode: none\n" in compose
    assert "      - artifacts:/srv/spider/artifacts\n" in compose
    assert "      - runtime-lock:/srv/spider/locks\n" in compose
    assert "chmod 0770 /srv/spider/artifacts /srv/spider/locks" not in compose
    assert "    cap_add: [CHOWN]\n" in compose
    assert compose.count("runtime-init:\n        condition: service_completed_successfully") == 2


def test_runtime_image_has_host_mapped_spider_identity() -> None:
    compose = (ROOT / "docker-compose.yml").read_text()
    dockerfile = (ROOT / "Dockerfile").read_text()

    assert compose.count("SPIDER_EXECUTOR_UID: ${SPIDER_EXECUTOR_UID:-1000}") == 4
    assert compose.count("SPIDER_EXECUTOR_GID: ${SPIDER_EXECUTOR_GID:-1000}") == 4
    assert "SPIDER_SCRIPTS_REMOTE_URL: git@github.com:cl0udarch1t3cts/spider-scripts.git" in compose
    assert (
        "${SPIDER_EXECUTOR_SSH_HOST_PATH:-/home/spider/.ssh}:/app/.ssh:ro" in compose
    )
    assert compose.count(":/app/.ssh:ro") == 1
    assert Settings().scripts_remote_url == "git@github.com:cl0udarch1t3cts/spider-scripts.git"
    assert "ARG SPIDER_EXECUTOR_UID" in dockerfile
    assert "ARG SPIDER_EXECUTOR_GID" in dockerfile
    assert 'useradd --uid "$SPIDER_EXECUTOR_UID"' in dockerfile
    assert "git openssh-client" in dockerfile
    assert "PYTHONPATH=/app/src" in dockerfile
    assert dockerfile.count("RUN uv sync") == 1
    assert 'command: ["python", "-m", "spider_executor.worker_main"]' in compose
