import json

import httpx
import pytest
from starlette.testclient import TestClient

from spider_doctor.codex_broker import BrokerSettings, create_app


def broker_client(
    handler,
    resolver=None,
    *,
    max_concurrent_requests=2,
    model_registry=None,
    openrouter_key=None,
    openrouter_requests_per_minute=15,
) -> TestClient:
    settings = BrokerSettings(
        client_token="scoped-client-token",
        allowed_model="gpt-5.4",
        max_concurrent_requests=max_concurrent_requests,
        requests_per_minute=20,
        model_registry=model_registry,
        openrouter_key=openrouter_key,
        openrouter_requests_per_minute=openrouter_requests_per_minute,
    )
    transport = httpx.MockTransport(handler)
    app = create_app(
        settings,
        credential_resolver=resolver
        or (
            lambda force_refresh=False: {
                "api_key": "upstream-oauth-token",
                "base_url": "https://chatgpt.com/backend-api/codex",
            }
        ),
        upstream_transport=transport,
    )
    return TestClient(app)


def test_broker_rejects_wrong_client_token_before_upstream() -> None:
    def must_not_run(_request):
        raise AssertionError("upstream must not be called")

    with broker_client(must_not_run) as client:
        response = client.post(
            "/v1/responses",
            headers={"authorization": "Bearer wrong"},
            json={"model": "gpt-5.4", "input": "hello"},
        )

    assert response.status_code == 401


def test_broker_readiness_requires_resolvable_codex_oauth() -> None:
    with broker_client(lambda _request: httpx.Response(500)) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_broker_rejects_model_outside_single_model_allowlist() -> None:
    def must_not_run(_request):
        raise AssertionError("upstream must not be called")

    with broker_client(must_not_run) as client:
        response = client.post(
            "/v1/responses",
            headers={"authorization": "Bearer scoped-client-token"},
            json={"model": "other-model", "input": "hello"},
        )

    assert response.status_code == 403


def test_broker_attaches_oauth_and_streams_codex_response() -> None:
    captured = {}

    def upstream(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["authorization"] = request.headers["authorization"]
        captured["originator"] = request.headers["originator"]
        captured["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            stream=httpx.ByteStream(b'data: {"type":"response.completed"}\n\n'),
        )

    with broker_client(upstream) as client:
        response = client.post(
            "/v1/responses",
            headers={"authorization": "Bearer scoped-client-token"},
            json={"model": "gpt-5.4", "input": "hello", "stream": True},
        )

    assert response.status_code == 200
    assert response.text == 'data: {"type":"response.completed"}\n\n'
    assert captured == {
        "url": "https://chatgpt.com/backend-api/codex/responses",
        "authorization": "Bearer upstream-oauth-token",
        "originator": "codex_cli_rs",
        "body": {"model": "gpt-5.4", "input": "hello", "stream": True},
    }


def test_broker_refreshes_once_after_upstream_401() -> None:
    refresh_calls = []
    upstream_calls = 0

    def resolver(force_refresh=False):
        refresh_calls.append(force_refresh)
        return {
            "api_key": "fresh" if force_refresh else "stale",
            "base_url": "https://chatgpt.com/backend-api/codex",
        }

    def upstream(request: httpx.Request) -> httpx.Response:
        nonlocal upstream_calls
        upstream_calls += 1
        if request.headers["authorization"] == "Bearer stale":
            return httpx.Response(401, stream=httpx.ByteStream(b"unauthorized"))
        return httpx.Response(200, stream=httpx.ByteStream(b'{"id":"ok"}'))

    with broker_client(upstream, resolver) as client:
        response = client.post(
            "/v1/responses",
            headers={"authorization": "Bearer scoped-client-token"},
            json={"model": "gpt-5.4", "input": "hello"},
        )

    assert response.status_code == 200
    assert response.json() == {"id": "ok"}
    assert refresh_calls == [False, True]
    assert upstream_calls == 2


def test_usage_requires_the_scoped_client_token() -> None:
    def must_not_run(_request):
        raise AssertionError("upstream must not be called")

    with broker_client(must_not_run) as client:
        response = client.get("/usage", headers={"authorization": "Bearer wrong"})

    assert response.status_code == 401


def test_usage_probes_the_provider_endpoint_and_normalizes_field_names() -> None:
    def upstream(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://chatgpt.com/backend-api/codex/usage"
        assert request.headers["authorization"] == "Bearer upstream-oauth-token"
        return httpx.Response(
            200,
            json={
                "rate_limits": {
                    "primary": {"usedPercent": 12.5, "windowDurationMins": 300, "resetsInSeconds": 900},
                    "secondary": {"usedPercent": 33.0, "windowDurationMins": 10080, "resetsInSeconds": 400000},
                }
            },
        )

    with broker_client(upstream) as client:
        response = client.get("/usage", headers={"authorization": "Bearer scoped-client-token"})

    assert response.status_code == 200
    assert response.json() == {
        "source": "api",
        "windows": [
            {"name": "primary", "used_percent": 12.5, "window_minutes": 300, "resets_in_seconds": 900},
            {"name": "secondary", "used_percent": 33.0, "window_minutes": 10080, "resets_in_seconds": 400000},
        ],
    }


def test_usage_normalizes_the_production_rate_limit_shape() -> None:
    # Shape observed live on 2026-08-23: singular rate_limit, *_window names,
    # window duration in seconds, reset as reset_after_seconds.
    def upstream(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "plan_type": "prolite",
                "rate_limit": {
                    "allowed": True,
                    "limit_reached": False,
                    "primary_window": {
                        "used_percent": 62,
                        "limit_window_seconds": 604800,
                        "reset_after_seconds": 5595,
                        "reset_at": 1787519686,
                    },
                    "secondary_window": None,
                },
                "additional_rate_limits": [],
            },
        )

    with broker_client(upstream) as client:
        response = client.get("/usage", headers={"authorization": "Bearer scoped-client-token"})

    assert response.status_code == 200
    assert response.json() == {
        "source": "api",
        "windows": [
            {
                "name": "primary",
                "used_percent": 62.0,
                "window_minutes": 10080,
                "resets_in_seconds": 5595,
            }
        ],
    }


def test_usage_falls_back_to_rate_limit_headers_from_proxied_responses() -> None:
    def upstream(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/usage"):
            return httpx.Response(404)
        return httpx.Response(
            200,
            headers={
                "content-type": "application/json",
                "x-codex-primary-used-percent": "7.0",
                "x-codex-secondary-used-percent": "21.5",
                "x-codex-secondary-window-minutes": "10080",
                "x-codex-secondary-resets-in-seconds": "300000",
            },
            stream=httpx.ByteStream(b'{"id":"ok"}'),
        )

    with broker_client(upstream) as client:
        client.post(
            "/v1/responses",
            headers={"authorization": "Bearer scoped-client-token"},
            json={"model": "gpt-5.4", "input": "hello"},
        )
        response = client.get("/usage", headers={"authorization": "Bearer scoped-client-token"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["source"] == "headers"
    assert payload["windows"] == [
        {"name": "primary", "used_percent": 7.0, "window_minutes": None, "resets_in_seconds": None},
        {
            "name": "secondary",
            "used_percent": 21.5,
            "window_minutes": 10080,
            "resets_in_seconds": 300000,
        },
    ]


def test_usage_reports_unavailable_when_no_source_exists() -> None:
    with broker_client(lambda _request: httpx.Response(404)) as client:
        response = client.get("/usage", headers={"authorization": "Bearer scoped-client-token"})

    assert response.status_code == 503


def test_broker_releases_concurrency_slot_when_stream_raises() -> None:
    class BrokenStream(httpx.AsyncByteStream):
        async def __aiter__(self):
            yield b"partial"
            raise RuntimeError("upstream stream broke")

    calls = 0

    def upstream(_request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(200, stream=BrokenStream())
        return httpx.Response(200, stream=httpx.ByteStream(b'{"id":"recovered"}'))

    with broker_client(upstream, max_concurrent_requests=1) as client:
        with pytest.raises(RuntimeError, match="upstream stream broke"):
            client.post(
                "/v1/responses",
                headers={"authorization": "Bearer scoped-client-token"},
                json={"model": "gpt-5.4", "input": "first"},
            )
        recovered = client.post(
            "/v1/responses",
            headers={"authorization": "Bearer scoped-client-token"},
            json={"model": "gpt-5.4", "input": "second"},
        )

    assert recovered.status_code == 200
    assert recovered.json() == {"id": "recovered"}


REGISTRY = {
    "gpt-5.4": {"upstream": "codex"},
    "qwen3-coder:free": {
        "upstream": "openrouter",
        "upstream_model": "qwen/qwen3-coder:free",
    },
}


def test_registry_routes_chat_completions_to_openrouter_with_key() -> None:
    captured = {}

    def upstream(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["authorization"] = request.headers["authorization"]
        captured["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            stream=httpx.ByteStream(b"data: [DONE]\n\n"),
        )

    def resolver(force_refresh=False):
        raise AssertionError("codex credentials must not be touched for openrouter")

    with broker_client(
        upstream, resolver, model_registry=REGISTRY, openrouter_key="or-secret"
    ) as client:
        response = client.post(
            "/v1/chat/completions",
            headers={"authorization": "Bearer scoped-client-token"},
            json={"model": "qwen3-coder:free", "messages": [], "stream": True},
        )

    assert response.status_code == 200
    assert response.text == "data: [DONE]\n\n"
    assert captured["url"] == "https://openrouter.ai/api/v1/chat/completions"
    assert captured["authorization"] == "Bearer or-secret"
    # The public model name is rewritten to the upstream's identifier.
    assert captured["body"]["model"] == "qwen/qwen3-coder:free"


def test_chat_completions_rejects_codex_routed_and_unknown_models() -> None:
    def must_not_run(_request):
        raise AssertionError("upstream must not be called")

    with broker_client(
        must_not_run, model_registry=REGISTRY, openrouter_key="or-secret"
    ) as client:
        headers = {"authorization": "Bearer scoped-client-token"}
        codex_model = client.post(
            "/v1/chat/completions", headers=headers, json={"model": "gpt-5.4"}
        )
        unknown = client.post(
            "/v1/chat/completions", headers=headers, json={"model": "nope"}
        )
        wrong_token = client.post(
            "/v1/chat/completions",
            headers={"authorization": "Bearer wrong"},
            json={"model": "qwen3-coder:free"},
        )

    assert codex_model.status_code == 403
    assert unknown.status_code == 403
    assert wrong_token.status_code == 401


def test_responses_route_rejects_openrouter_routed_model() -> None:
    def must_not_run(_request):
        raise AssertionError("upstream must not be called")

    with broker_client(
        must_not_run, model_registry=REGISTRY, openrouter_key="or-secret"
    ) as client:
        response = client.post(
            "/v1/responses",
            headers={"authorization": "Bearer scoped-client-token"},
            json={"model": "qwen3-coder:free", "input": "hello"},
        )

    assert response.status_code == 403


def test_registry_keeps_codex_route_working_unchanged() -> None:
    def upstream(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://chatgpt.com/backend-api/codex/responses"
        return httpx.Response(200, stream=httpx.ByteStream(b'{"id":"ok"}'))

    with broker_client(
        upstream, model_registry=REGISTRY, openrouter_key="or-secret"
    ) as client:
        response = client.post(
            "/v1/responses",
            headers={"authorization": "Bearer scoped-client-token"},
            json={"model": "gpt-5.4", "input": "hello"},
        )

    assert response.status_code == 200


def test_openrouter_rate_limit_returns_429_with_retry_after() -> None:
    def upstream(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, stream=httpx.ByteStream(b"{}"))

    with broker_client(
        upstream,
        model_registry=REGISTRY,
        openrouter_key="or-secret",
        openrouter_requests_per_minute=1,
    ) as client:
        headers = {"authorization": "Bearer scoped-client-token"}
        first = client.post(
            "/v1/chat/completions", headers=headers, json={"model": "qwen3-coder:free"}
        )
        second = client.post(
            "/v1/chat/completions", headers=headers, json={"model": "qwen3-coder:free"}
        )

    assert first.status_code == 200
    assert second.status_code == 429
    assert "retry-after" in second.headers


def test_settings_reject_openrouter_registry_entries_without_key() -> None:
    with pytest.raises(ValueError, match="openrouter"):
        BrokerSettings(
            client_token="token",
            allowed_model="gpt-5.4",
            model_registry=REGISTRY,
            openrouter_key=None,
        )
