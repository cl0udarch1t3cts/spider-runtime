from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

SECONDS_PER_DAY = 86_400


@dataclass(frozen=True)
class BudgetDecision:
    allowed: bool
    detail: str


@dataclass(frozen=True)
class UsageWindow:
    name: str
    used_percent: float
    window_minutes: int | None
    resets_in_seconds: int | None


class SubscriptionBudgetGate:
    """Paces weekly subscription spend before each Hermes launch.

    The weekly contingent is split into a per-day job allowance plus a
    development reserve: by day N of the window, jobs may have consumed at
    most N * daily_percent of the subscription, and never more than
    100 - reserve_percent overall. Usage is read from the broker, which
    holds the only credential able to query the provider; if usage cannot
    be determined the gate fails open so a broker outage does not stall
    repairs.
    """

    def __init__(
        self,
        usage_url: str,
        client_token: str,
        *,
        daily_percent: float = 10.0,
        reserve_percent: float = 30.0,
        cache_seconds: float = 300.0,
        timeout_seconds: float = 30.0,
        transport: httpx.BaseTransport | None = None,
        overrides: Callable[[], dict] | None = None,
    ) -> None:
        if not 0 < daily_percent <= 100:
            raise ValueError("daily budget percent must be within (0, 100]")
        if not 0 <= reserve_percent < 100:
            raise ValueError("development reserve percent must be within [0, 100)")
        self.usage_url = usage_url
        self.daily_percent = daily_percent
        self.reserve_percent = reserve_percent
        self.cache_seconds = cache_seconds
        self.overrides = overrides
        self._client = httpx.Client(
            headers={"Authorization": f"Bearer {client_token}"},
            timeout=httpx.Timeout(timeout_seconds, connect=20.0),
            transport=transport,
        )
        self._cached: tuple[float, BudgetDecision] | None = None
        self._lock = threading.Lock()

    def check(self) -> BudgetDecision:
        with self._lock:
            now = time.monotonic()
            if self._cached is not None and now - self._cached[0] < self.cache_seconds:
                return self._cached[1]
            decision = self._evaluate()
            self._cached = (now, decision)
        if decision.allowed:
            logger.info("Doctor budget decision: proceed (%s)", decision.detail)
        else:
            logger.warning("Doctor budget decision: defer (%s)", decision.detail)
        return decision

    def _current_percents(self) -> tuple[float, float]:
        daily, reserve = self.daily_percent, self.reserve_percent
        if self.overrides is not None:
            try:
                override = self.overrides() or {}
                candidate_daily = override.get("daily_percent")
                candidate_reserve = override.get("reserve_percent")
                if isinstance(candidate_daily, (int, float)) and 0 < candidate_daily <= 100:
                    daily = float(candidate_daily)
                if isinstance(candidate_reserve, (int, float)) and 0 <= candidate_reserve < 100:
                    reserve = float(candidate_reserve)
            except Exception as exc:  # noqa: BLE001 - overrides must not stall repairs
                logger.warning("budget override unavailable, using configured percents: %s", exc)
        return daily, reserve

    def _evaluate(self) -> BudgetDecision:
        try:
            source, windows = self._fetch_usage()
        except Exception as exc:  # noqa: BLE001 - a usage outage must not stall repairs
            return BudgetDecision(
                True, f"subscription usage unavailable ({type(exc).__name__}: {exc}); failing open"
            )
        weekly = _weekly_window(windows)
        if weekly is None:
            return BudgetDecision(True, "subscription usage reported no windows; failing open")

        daily_percent, reserve_percent = self._current_percents()
        cap = 100.0 - reserve_percent
        if weekly.window_minutes and weekly.resets_in_seconds is not None:
            window_seconds = weekly.window_minutes * 60
            elapsed = min(window_seconds, max(0, window_seconds - weekly.resets_in_seconds))
            total_days = max(1, round(window_seconds / SECONDS_PER_DAY))
            day = min(int(elapsed // SECONDS_PER_DAY) + 1, total_days)
            allowed = min(cap, daily_percent * day)
            pacing = (
                f"day {day}/{total_days} of the {weekly.name} window, "
                f"resets in {_format_duration(weekly.resets_in_seconds)}"
            )
        else:
            allowed = cap
            pacing = f"{weekly.name} window timing unknown, enforcing the weekly cap only"
        detail = (
            f"usage {weekly.used_percent:.1f}% of {allowed:.1f}% allowed via {source}; "
            f"{pacing}; daily job budget {daily_percent:g}%, "
            f"development reserve {reserve_percent:g}%"
        )
        return BudgetDecision(weekly.used_percent < allowed, detail)

    def _fetch_usage(self) -> tuple[str, list[UsageWindow]]:
        response = self._client.get(self.usage_url)
        response.raise_for_status()
        payload = response.json()
        windows = [
            UsageWindow(
                name=str(entry.get("name", "unknown")),
                used_percent=float(entry["used_percent"]),
                window_minutes=_optional_int(entry.get("window_minutes")),
                resets_in_seconds=_optional_int(entry.get("resets_in_seconds")),
            )
            for entry in payload.get("windows", [])
            if isinstance(entry, dict) and isinstance(entry.get("used_percent"), (int, float))
        ]
        return str(payload.get("source", "unknown")), windows


def _optional_int(value: object) -> int | None:
    return int(value) if isinstance(value, (int, float)) else None


def _weekly_window(windows: list[UsageWindow]) -> UsageWindow | None:
    if not windows:
        return None
    with_duration = [window for window in windows if window.window_minutes]
    if with_duration:
        return max(with_duration, key=lambda window: window.window_minutes or 0)
    for window in windows:
        if window.name in ("secondary", "weekly"):
            return window
    # Without timing metadata the most-consumed window is the safe choice.
    return max(windows, key=lambda window: window.used_percent)


def _format_duration(seconds: int) -> str:
    days, remainder = divmod(max(0, seconds), SECONDS_PER_DAY)
    hours = remainder // 3600
    return f"{days}d{hours}h" if days else f"{hours}h{(remainder % 3600) // 60}m"
