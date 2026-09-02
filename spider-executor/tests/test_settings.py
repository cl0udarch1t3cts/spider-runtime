import socket

from spider_executor.settings import Settings


def test_worker_identity_and_concurrency_defaults(monkeypatch) -> None:
    monkeypatch.delenv("SPIDER_WORKER_ID", raising=False)
    monkeypatch.delenv("SPIDER_WORKER_CONCURRENCY", raising=False)
    settings = Settings(_env_file=None)

    assert settings.worker_id == f"executor-{socket.gethostname()}"
    assert settings.worker_concurrency == 1


def test_worker_settings_env_overrides(monkeypatch) -> None:
    monkeypatch.setenv("SPIDER_WORKER_ID", "executor-a")
    monkeypatch.setenv("SPIDER_WORKER_CONCURRENCY", "10")
    settings = Settings(_env_file=None)

    assert settings.worker_id == "executor-a"
    assert settings.worker_concurrency == 10
