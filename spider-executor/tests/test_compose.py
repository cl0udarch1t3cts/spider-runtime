from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_runtime_volumes_are_initialized_for_the_runtime_user() -> None:
    compose = (ROOT / "docker-compose.yml").read_text()

    assert "  runtime-init:\n" in compose
    assert "SPIDER_EXECUTOR_UID: ${SPIDER_EXECUTOR_UID:-1000}" in compose
    assert "SPIDER_EXECUTOR_GID: ${SPIDER_EXECUTOR_GID:-1000}" in compose
    assert '    user: "0:0"\n' in compose
    assert "    network_mode: none\n" in compose
    assert "      - artifacts:/srv/spider/artifacts\n" in compose
    assert "      - runtime-lock:/srv/spider/locks\n" in compose
    assert compose.index("chmod 0770 /srv/spider/artifacts /srv/spider/locks") < compose.index(
        "chown -R spider:spider /srv/spider/artifacts /srv/spider/locks"
    )
    assert compose.count("runtime-init:\n        condition: service_completed_successfully") == 2


def test_runtime_image_has_host_mapped_spider_identity() -> None:
    compose = (ROOT / "docker-compose.yml").read_text()
    dockerfile = (ROOT / "Dockerfile").read_text()

    assert compose.count("SPIDER_EXECUTOR_UID: ${SPIDER_EXECUTOR_UID:-1000}") == 4
    assert compose.count("SPIDER_EXECUTOR_GID: ${SPIDER_EXECUTOR_GID:-1000}") == 4
    assert "ARG SPIDER_EXECUTOR_UID" in dockerfile
    assert "ARG SPIDER_EXECUTOR_GID" in dockerfile
    assert 'useradd --uid "$SPIDER_EXECUTOR_UID"' in dockerfile
