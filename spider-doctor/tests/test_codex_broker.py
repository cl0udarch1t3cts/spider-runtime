import json

import httpx
import pytest
from starlette.testclient import TestClient

from spider_doctor.codex_broker import BrokerSettings, create_app


def broker_client(handler, resolver=None, *, max_concurrent_requests=2) -> TestClient:
    settings = BrokerSettings(
        client_token="scoped-client-token",
        allowed_model="gpt-5.4",
        max_concurrent_requests=max_concurrent_requests,
        requests_per_minute=20,
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
