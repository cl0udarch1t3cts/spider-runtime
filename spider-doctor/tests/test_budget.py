import json

import httpx
import pytest

from spider_doctor.budget import SubscriptionBudgetGate

WEEKLY_MINUTES = 7 * 24 * 60


def usage_gate(payload, *, status_code=200, daily=10.0, reserve=30.0, calls=None):
    def handler(request: httpx.Request) -> httpx.Response:
        if calls is not None:
            calls.append(request)
        assert request.headers["authorization"] == "Bearer proxy-token"
        return httpx.Response(status_code, content=json.dumps(payload))

    return SubscriptionBudgetGate(
        "http://broker:8645/usage",
        "proxy-token",
        daily_percent=daily,
        reserve_percent=reserve,
        transport=httpx.MockTransport(handler),
    )


def weekly_payload(used_percent: float, *, elapsed_days: float, source="api") -> dict:
    return {
        "source": source,
        "windows": [
            {"name": "primary", "used_percent": 1.0, "window_minutes": 300, "resets_in_seconds": 60},
            {
                "name": "secondary",
                "used_percent": used_percent,
                "window_minutes": WEEKLY_MINUTES,
                "resets_in_seconds": int((7 - elapsed_days) * 86_400),
            },
        ],
    }


def test_gate_allows_usage_under_the_daily_paced_allowance() -> None:
    gate = usage_gate(weekly_payload(25.0, elapsed_days=2.5))

    decision = gate.check()

    assert decision.allowed
    assert "usage 25.0% of 30.0% allowed" in decision.detail
    assert "day 3/7" in decision.detail


def test_gate_defers_when_usage_reaches_the_daily_allowance() -> None:
    gate = usage_gate(weekly_payload(12.0, elapsed_days=0.5))

    decision = gate.check()

    assert not decision.allowed
    assert "usage 12.0% of 10.0% allowed" in decision.detail


def test_gate_enforces_the_development_reserve_cap_late_in_the_window() -> None:
    gate = usage_gate(weekly_payload(71.0, elapsed_days=6.9))

    decision = gate.check()

    assert not decision.allowed
    assert "of 70.0% allowed" in decision.detail


def test_gate_uses_the_longest_window_as_the_weekly_contingent() -> None:
    gate = usage_gate(weekly_payload(95.0, elapsed_days=3.0))
    # The 5h primary window sits at 1% but must not be the one gated on.
    decision = gate.check()

    assert not decision.allowed
    assert "usage 95.0%" in decision.detail


def test_gate_without_window_timing_enforces_only_the_weekly_cap() -> None:
    gate = usage_gate({"source": "headers", "windows": [{"name": "secondary", "used_percent": 50.0}]})

    decision = gate.check()

    assert decision.allowed
    assert "of 70.0% allowed" in decision.detail
    assert "weekly cap only" in decision.detail


def test_gate_fails_open_when_usage_is_unavailable() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("broker down")

    gate = SubscriptionBudgetGate(
        "http://broker:8645/usage",
        "proxy-token",
        transport=httpx.MockTransport(handler),
    )

    decision = gate.check()

    assert decision.allowed
    assert "failing open" in decision.detail


def test_gate_fails_open_on_error_status() -> None:
    gate = usage_gate({"error": "usage unavailable"}, status_code=503)

    decision = gate.check()

    assert decision.allowed
    assert "failing open" in decision.detail


def test_gate_caches_the_decision_between_checks() -> None:
    calls: list[httpx.Request] = []
    gate = usage_gate(weekly_payload(25.0, elapsed_days=2.5), calls=calls)

    first = gate.check()
    second = gate.check()

    assert first == second
    assert len(calls) == 1


def test_gate_rejects_nonsensical_budget_configuration() -> None:
    with pytest.raises(ValueError):
        SubscriptionBudgetGate("http://broker:8645/usage", "proxy-token", daily_percent=0)
    with pytest.raises(ValueError):
        SubscriptionBudgetGate("http://broker:8645/usage", "proxy-token", reserve_percent=100)
