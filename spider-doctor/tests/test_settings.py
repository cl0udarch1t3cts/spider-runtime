from spider_doctor.settings import Settings


def test_default_lease_outlives_agent_timeout_with_completion_margin() -> None:
    settings = Settings()

    assert settings.lease_minutes * 60 >= settings.agent_timeout_seconds + 300
