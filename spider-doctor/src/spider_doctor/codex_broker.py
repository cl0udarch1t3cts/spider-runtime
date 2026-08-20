from __future__ import annotations

import argparse
import asyncio
import base64
import binascii
import hmac
import importlib
import json
import os
import time
from collections import deque
from collections.abc import Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import uvicorn
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse
from starlette.routing import Route

CredentialResolver = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class BrokerSettings:
    client_token: str
    allowed_model: str
    max_concurrent_requests: int = 2
    requests_per_minute: int = 20
    max_request_bytes: int = 2 * 1024 * 1024

    def __post_init__(self) -> None:
        if not self.client_token.strip():
            raise ValueError("broker client token is required")
        if not self.allowed_model.strip():
            raise ValueError("broker allowed model is required")
        if self.max_concurrent_requests < 1 or self.requests_per_minute < 1:
            raise ValueError("broker limits must be positive")


class RateWindow:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self._calls: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def allow(self) -> bool:
        async with self._lock:
            now = time.monotonic()
            while self._calls and self._calls[0] <= now - 60:
                self._calls.popleft()
            if len(self._calls) >= self.limit:
                return False
            self._calls.append(now)
            return True


def _account_id(access_token: str) -> str | None:
    try:
        encoded = access_token.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
        value = claims.get("https://api.openai.com/auth", {}).get("chatgpt_account_id")
        return value if isinstance(value, str) and value else None
    except (IndexError, KeyError, TypeError, ValueError, UnicodeDecodeError, binascii.Error):
        return None


def _upstream_headers(access_token: str) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "text/event-stream, application/json",
        "Content-Type": "application/json",
        "originator": "codex_cli_rs",
        "User-Agent": "codex_cli_rs/0.0.0 (Spider Doctor Broker)",
    }
    account_id = _account_id(access_token)
    if account_id:
        headers["ChatGPT-Account-ID"] = account_id
    return headers


def create_app(
    settings: BrokerSettings,
    *,
    credential_resolver: CredentialResolver,
    upstream_transport: httpx.AsyncBaseTransport | None = None,
) -> Starlette:
    concurrency = asyncio.Semaphore(settings.max_concurrent_requests)
    rate = RateWindow(settings.requests_per_minute)

    @asynccontextmanager
    async def lifespan(app: Starlette):
        timeout = httpx.Timeout(1900.0, connect=20.0, pool=5.0)
        app.state.upstream = httpx.AsyncClient(transport=upstream_transport, timeout=timeout)
        yield
        await app.state.upstream.aclose()

    async def health(_request: Request) -> Response:
        return JSONResponse({"status": "ok"})

    async def ready(_request: Request) -> Response:
        try:
            credentials = await run_in_threadpool(
                credential_resolver, force_refresh=False
            )
        except Exception:  # noqa: BLE001 - readiness converts auth/refresh failures to 503
            return JSONResponse({"status": "oauth unavailable"}, status_code=503)
        token = str(credentials.get("api_key", "") or "").strip()
        base_url = str(credentials.get("base_url", "") or "").rstrip("/")
        if not token or base_url != "https://chatgpt.com/backend-api/codex":
            return JSONResponse({"status": "oauth unavailable"}, status_code=503)
        return JSONResponse({"status": "ready"})

    async def responses(request: Request) -> Response:
        supplied = request.headers.get("authorization", "")
        expected = f"Bearer {settings.client_token}"
        if not hmac.compare_digest(supplied, expected):
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        if request.headers.get("content-length"):
            try:
                if int(request.headers["content-length"]) > settings.max_request_bytes:
                    return JSONResponse({"error": "request too large"}, status_code=413)
            except ValueError:
                return JSONResponse({"error": "invalid content-length"}, status_code=400)
        body = await request.body()
        if len(body) > settings.max_request_bytes:
            return JSONResponse({"error": "request too large"}, status_code=413)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return JSONResponse({"error": "invalid JSON"}, status_code=400)
        if not isinstance(payload, dict) or payload.get("model") != settings.allowed_model:
            return JSONResponse({"error": "model not allowed"}, status_code=403)
        if not await rate.allow():
            return JSONResponse({"error": "rate limit exceeded"}, status_code=429)

        await concurrency.acquire()
        handed_off = False
        try:
            response: httpx.Response | None = None
            for force_refresh in (False, True):
                credentials = await run_in_threadpool(
                    credential_resolver, force_refresh=force_refresh
                )
                token = str(credentials.get("api_key", "") or "").strip()
                base_url = str(credentials.get("base_url", "") or "").rstrip("/")
                if not token or base_url != "https://chatgpt.com/backend-api/codex":
                    return JSONResponse({"error": "broker credential unavailable"}, status_code=503)
                upstream_request = request.app.state.upstream.build_request(
                    "POST",
                    f"{base_url}/responses",
                    headers=_upstream_headers(token),
                    content=body,
                )
                current = await request.app.state.upstream.send(upstream_request, stream=True)
                if current.status_code != 401 or force_refresh:
                    response = current
                    break
                await current.aclose()
            assert response is not None
            headers = {}
            for name in ("content-type", "x-request-id", "openai-processing-ms"):
                if name in response.headers:
                    headers[name] = response.headers[name]

            async def stream_body():
                try:
                    async for chunk in response.aiter_bytes():
                        yield chunk
                finally:
                    try:
                        await response.aclose()
                    finally:
                        concurrency.release()

            result = StreamingResponse(
                stream_body(),
                status_code=response.status_code,
                headers=headers,
            )
            handed_off = True
            return result
        finally:
            if not handed_off:
                concurrency.release()

    return Starlette(
        routes=[
            Route("/health/live", health, methods=["GET"]),
            Route("/health/ready", ready, methods=["GET"]),
            Route("/v1/responses", responses, methods=["POST"]),
        ],
        lifespan=lifespan,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Restricted OpenAI Codex subscription broker")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8645)
    args = parser.parse_args()
    token_file = Path(os.environ["SPIDER_BROKER_CLIENT_TOKEN_FILE"])
    if not token_file.is_file() or token_file.stat().st_size == 0:
        raise SystemExit("broker client token file is missing or empty")
    settings = BrokerSettings(
        client_token=token_file.read_text().strip(),
        allowed_model=os.environ.get("SPIDER_BROKER_ALLOWED_MODEL", "gpt-5.4"),
        max_concurrent_requests=int(os.environ.get("SPIDER_BROKER_MAX_CONCURRENT", "2")),
        requests_per_minute=int(os.environ.get("SPIDER_BROKER_REQUESTS_PER_MINUTE", "20")),
    )
    auth_module = importlib.import_module("hermes_cli.auth")
    resolve_codex_runtime_credentials = auth_module.resolve_codex_runtime_credentials

    app = create_app(settings, credential_resolver=resolve_codex_runtime_credentials)
    uvicorn.run(app, host=args.host, port=args.port, access_log=False)


if __name__ == "__main__":
    main()
