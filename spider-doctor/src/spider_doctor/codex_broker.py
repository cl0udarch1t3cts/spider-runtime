from __future__ import annotations

import argparse
import asyncio
import base64
import binascii
import hmac
import importlib
import json
import logging
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

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BrokerSettings:
    client_token: str
    allowed_model: str
    max_concurrent_requests: int = 2
    requests_per_minute: int = 20
    max_request_bytes: int = 2 * 1024 * 1024
    # Optional multi-provider registry: public model name -> {"upstream":
    # "codex"|"openrouter", "upstream_model": optional rewrite}. Absent, the
    # broker behaves exactly as before: allowed_model, codex only (ADR-008).
    model_registry: dict[str, dict[str, str]] | None = None
    openrouter_key: str | None = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_requests_per_minute: int = 15
    openrouter_max_concurrent: int = 2

    def __post_init__(self) -> None:
        if not self.client_token.strip():
            raise ValueError("broker client token is required")
        if not self.allowed_model.strip():
            raise ValueError("broker allowed model is required")
        if self.max_concurrent_requests < 1 or self.requests_per_minute < 1:
            raise ValueError("broker limits must be positive")
        if self.openrouter_max_concurrent < 1 or self.openrouter_requests_per_minute < 1:
            raise ValueError("broker limits must be positive")
        for name, entry in (self.model_registry or {}).items():
            if not isinstance(entry, dict) or entry.get("upstream") not in ("codex", "openrouter"):
                raise ValueError(f"model registry entry {name!r} needs upstream codex or openrouter")
            if entry["upstream"] == "openrouter" and not (self.openrouter_key or "").strip():
                raise ValueError(f"model registry entry {name!r} routes to openrouter but no key is configured")

    def models(self) -> dict[str, dict[str, str]]:
        return self.model_registry or {self.allowed_model: {"upstream": "codex"}}


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


_USAGE_USED_KEYS = ("used_percent", "usedPercent")
_USAGE_WINDOW_KEYS = (
    "window_minutes",
    "windowMinutes",
    "window_duration_mins",
    "windowDurationMins",
)
_USAGE_WINDOW_SECONDS_KEYS = ("limit_window_seconds", "limitWindowSeconds")
_USAGE_RESET_SECONDS_KEYS = ("resets_in_seconds", "resetsInSeconds", "reset_after_seconds")
_USAGE_RESET_AT_KEYS = ("resets_at", "resetsAt", "reset_at", "resetAt")


def _first_number(entry: dict[str, Any], keys: tuple[str, ...]) -> float | None:
    for key in keys:
        value = entry.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
    return None


def _usage_window(name: str, entry: Any, now: float) -> dict[str, Any] | None:
    if not isinstance(entry, dict):
        return None
    used_percent = _first_number(entry, _USAGE_USED_KEYS)
    if used_percent is None:
        return None
    window_minutes = _first_number(entry, _USAGE_WINDOW_KEYS)
    if window_minutes is None:
        window_seconds = _first_number(entry, _USAGE_WINDOW_SECONDS_KEYS)
        if window_seconds is not None:
            window_minutes = window_seconds / 60
    resets_in = _first_number(entry, _USAGE_RESET_SECONDS_KEYS)
    if resets_in is None:
        resets_at = _first_number(entry, _USAGE_RESET_AT_KEYS)
        if resets_at is not None:
            resets_in = max(0.0, resets_at - now)
    return {
        "name": name,
        "used_percent": used_percent,
        "window_minutes": int(window_minutes) if window_minutes is not None else None,
        "resets_in_seconds": int(resets_in) if resets_in is not None else None,
    }


def _windows_from_usage_payload(payload: Any, now: float) -> list[dict[str, Any]]:
    """Tolerantly normalize the provider usage endpoint (snake_case or camelCase)."""
    if not isinstance(payload, dict):
        return []
    container = (
        payload.get("rate_limits")
        or payload.get("rateLimits")
        or payload.get("rate_limit")
        or payload.get("rateLimit")
        or payload
    )
    if not isinstance(container, dict):
        return []
    windows = []
    for name, entry in container.items():
        window = _usage_window(str(name).removesuffix("_window").removesuffix("Window"), entry, now)
        if window is not None:
            windows.append(window)
    return windows


def _windows_from_headers(headers: httpx.Headers) -> list[dict[str, Any]]:
    """Extract the rate-limit snapshot attached to proxied Codex responses."""
    windows = []
    for name in ("primary", "secondary"):
        entry: dict[str, Any] = {}
        for field, header in (
            ("used_percent", f"x-codex-{name}-used-percent"),
            ("window_minutes", f"x-codex-{name}-window-minutes"),
            ("resets_in_seconds", f"x-codex-{name}-resets-in-seconds"),
        ):
            raw = headers.get(header)
            if raw is None:
                continue
            try:
                entry[field] = float(raw)
            except ValueError:
                continue
        window = _usage_window(name, entry, time.time())
        if window is not None:
            windows.append(window)
    return windows


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
    openrouter_concurrency = asyncio.Semaphore(settings.openrouter_max_concurrent)
    openrouter_rate = RateWindow(settings.openrouter_requests_per_minute)

    @asynccontextmanager
    async def lifespan(app: Starlette):
        timeout = httpx.Timeout(1900.0, connect=20.0, pool=5.0)
        app.state.upstream = httpx.AsyncClient(transport=upstream_transport, timeout=timeout)
        app.state.usage_headers = None
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

    async def _guarded_payload(
        request: Request, *, upstream_name: str
    ) -> tuple[dict | None, dict | None, Response | None]:
        """Shared client-token, size, JSON, and model-routing checks."""
        supplied = request.headers.get("authorization", "")
        expected = f"Bearer {settings.client_token}"
        if not hmac.compare_digest(supplied, expected):
            return None, None, JSONResponse({"error": "unauthorized"}, status_code=401)
        if request.headers.get("content-length"):
            try:
                if int(request.headers["content-length"]) > settings.max_request_bytes:
                    return None, None, JSONResponse({"error": "request too large"}, status_code=413)
            except ValueError:
                return None, None, JSONResponse({"error": "invalid content-length"}, status_code=400)
        body = await request.body()
        if len(body) > settings.max_request_bytes:
            return None, None, JSONResponse({"error": "request too large"}, status_code=413)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return None, None, JSONResponse({"error": "invalid JSON"}, status_code=400)
        entry = settings.models().get(payload.get("model")) if isinstance(payload, dict) else None
        if entry is None or entry.get("upstream") != upstream_name:
            return None, None, JSONResponse({"error": "model not allowed"}, status_code=403)
        return payload, entry, None

    async def responses(request: Request) -> Response:
        payload, _entry, error = await _guarded_payload(request, upstream_name="codex")
        if error is not None:
            return error
        body = json.dumps(payload).encode()
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
            snapshot = _windows_from_headers(response.headers)
            if snapshot:
                request.app.state.usage_headers = {
                    "windows": snapshot,
                    "captured_at": time.time(),
                }
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

    async def chat_completions(request: Request) -> Response:
        payload, entry, error = await _guarded_payload(request, upstream_name="openrouter")
        if error is not None:
            return error
        if not await openrouter_rate.allow():
            return JSONResponse(
                {"error": "rate limited"}, status_code=429, headers={"Retry-After": "20"}
            )
        payload["model"] = entry.get("upstream_model") or payload["model"]
        headers = {
            "Authorization": f"Bearer {settings.openrouter_key}",
            "Accept": "text/event-stream, application/json",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/cl0udarch1t3cts/spider-runtime",
            "X-Title": "Spider Doctor",
        }
        await openrouter_concurrency.acquire()
        handed_off = False
        try:
            upstream_request = request.app.state.upstream.build_request(
                "POST",
                f"{settings.openrouter_base_url.rstrip('/')}/chat/completions",
                headers=headers,
                content=json.dumps(payload).encode(),
            )
            response = await request.app.state.upstream.send(upstream_request, stream=True)
            passthrough = {}
            for name in ("content-type", "x-request-id"):
                if name in response.headers:
                    passthrough[name] = response.headers[name]

            async def stream_body():
                try:
                    async for chunk in response.aiter_bytes():
                        yield chunk
                finally:
                    try:
                        await response.aclose()
                    finally:
                        openrouter_concurrency.release()

            result = StreamingResponse(
                stream_body(), status_code=response.status_code, headers=passthrough
            )
            handed_off = True
            return result
        finally:
            if not handed_off:
                openrouter_concurrency.release()

    async def _openrouter_credits(request: Request) -> dict | None:
        if not (settings.openrouter_key or "").strip():
            return None
        try:
            response = await request.app.state.upstream.get(
                f"{settings.openrouter_base_url.rstrip('/')}/credits",
                headers={"Authorization": f"Bearer {settings.openrouter_key}"},
                timeout=httpx.Timeout(10.0, connect=5.0),
            )
            if response.status_code != 200:
                return None
            data = response.json().get("data")
            total = data.get("total_credits") if isinstance(data, dict) else None
            used = data.get("total_usage") if isinstance(data, dict) else None
            if isinstance(total, (int, float)) and isinstance(used, (int, float)):
                return {"total_credits": float(total), "total_usage": float(used)}
        except Exception as exc:  # noqa: BLE001 - credits are informational only
            logger.warning("openrouter credits probe failed: %s", exc)
        return None

    async def usage(request: Request) -> Response:
        supplied = request.headers.get("authorization", "")
        expected = f"Bearer {settings.client_token}"
        if not hmac.compare_digest(supplied, expected):
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        # Prefer a live probe of the provider usage endpoint; fall back to the
        # rate-limit snapshot captured from the most recent proxied response.
        try:
            credentials = await run_in_threadpool(credential_resolver, force_refresh=False)
            token = str(credentials.get("api_key", "") or "").strip()
            base_url = str(credentials.get("base_url", "") or "").rstrip("/")
            if token and base_url == "https://chatgpt.com/backend-api/codex":
                upstream_response = await request.app.state.upstream.get(
                    f"{base_url}/usage",
                    headers=_upstream_headers(token),
                    timeout=httpx.Timeout(30.0, connect=20.0),
                )
                if upstream_response.status_code == 200:
                    windows = _windows_from_usage_payload(upstream_response.json(), time.time())
                    if windows:
                        payload = {"source": "api", "windows": windows}
                        credits = await _openrouter_credits(request)
                        if credits is not None:
                            payload["openrouter"] = credits
                        return JSONResponse(payload)
                    logger.warning("usage probe returned 200 but no parseable windows")
                else:
                    logger.warning(
                        "usage probe returned HTTP %s", upstream_response.status_code
                    )
        except Exception as exc:  # noqa: BLE001 - a failed probe falls back to the header snapshot
            logger.warning("usage probe failed: %s", exc)
        snapshot = request.app.state.usage_headers
        if snapshot is not None:
            payload = {
                "source": "headers",
                "age_seconds": int(time.time() - snapshot["captured_at"]),
                "windows": snapshot["windows"],
            }
            credits = await _openrouter_credits(request)
            if credits is not None:
                payload["openrouter"] = credits
            return JSONResponse(payload)
        return JSONResponse({"error": "usage unavailable"}, status_code=503)

    return Starlette(
        routes=[
            Route("/health/live", health, methods=["GET"]),
            Route("/health/ready", ready, methods=["GET"]),
            Route("/usage", usage, methods=["GET"]),
            Route("/v1/responses", responses, methods=["POST"]),
            Route("/v1/chat/completions", chat_completions, methods=["POST"]),
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
    model_registry = None
    models_file = os.environ.get("SPIDER_BROKER_MODELS_FILE", "")
    if models_file and Path(models_file).is_file():
        model_registry = json.loads(Path(models_file).read_text())
    openrouter_key = None
    key_file = os.environ.get("SPIDER_BROKER_OPENROUTER_KEY_FILE", "")
    if key_file and Path(key_file).is_file():
        openrouter_key = Path(key_file).read_text().strip() or None
    settings = BrokerSettings(
        client_token=token_file.read_text().strip(),
        allowed_model=os.environ.get("SPIDER_BROKER_ALLOWED_MODEL", "gpt-5.4"),
        max_concurrent_requests=int(os.environ.get("SPIDER_BROKER_MAX_CONCURRENT", "2")),
        requests_per_minute=int(os.environ.get("SPIDER_BROKER_REQUESTS_PER_MINUTE", "20")),
        model_registry=model_registry,
        openrouter_key=openrouter_key,
        openrouter_requests_per_minute=int(
            os.environ.get("SPIDER_BROKER_OPENROUTER_REQUESTS_PER_MINUTE", "15")
        ),
    )
    auth_module = importlib.import_module("hermes_cli.auth")
    resolve_codex_runtime_credentials = auth_module.resolve_codex_runtime_credentials

    app = create_app(settings, credential_resolver=resolve_codex_runtime_credentials)
    uvicorn.run(app, host=args.host, port=args.port, access_log=False)


if __name__ == "__main__":
    main()
