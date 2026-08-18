from spider_doctor.settings import Settings


def test_proxy_token_file_uses_doctor_environment_prefix(monkeypatch, tmp_path) -> None:
    token_file = tmp_path / "proxy-token"
    monkeypatch.setenv("SPIDER_DOCTOR_PROXY_TOKEN_FILE", str(token_file))

    settings = Settings()

    assert settings.proxy_token_file == token_file


def test_default_lease_outlives_agent_timeout_with_completion_margin() -> None:
    settings = Settings()

    assert settings.lease_minutes * 60 >= settings.agent_timeout_seconds + 300
