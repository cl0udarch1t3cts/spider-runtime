"""Per-attempt model selection for Doctor tasks (ADR-008).

The policy lives as data in ``runtime_state {_id: "model_policy"}`` so the
console can edit it without a redeploy:

    {
      "rules": [{"attempt": 1, "model": "qwen3-coder:free"},
                {"attempt": 2, "model": "gpt-5.4"}],
      "split": [{"model": "gpt-5.4", "weight": 50}, ...],
      "default_model": "gpt-5.4",
      "budget_fallback_model": "deepseek-r1:free"
    }

``rules`` (attempt-based) wins over ``split`` (weighted, deterministic by
task id hash) over ``default_model`` over the configured codex model. Any
malformed piece degrades to the next mechanism — a broken policy document
must never stall the Doctor.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

CODEX_PROVIDER = "doctor-codex"
OPENROUTER_PROVIDER = "doctor-openrouter"


@dataclass(frozen=True)
class ModelChoice:
    model: str
    provider: str
    budget_gated: bool
    reason: str


def _choice(model: str, codex_model: str, reason: str) -> ModelChoice:
    gated = model == codex_model
    return ModelChoice(
        model=model,
        provider=CODEX_PROVIDER if gated else OPENROUTER_PROVIDER,
        budget_gated=gated,
        reason=reason,
    )


def _from_rules(rules: object, attempt: int) -> str | None:
    if not isinstance(rules, list):
        return None
    best_attempt = None
    best_model = None
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        rule_attempt = rule.get("attempt")
        model = rule.get("model")
        if not isinstance(rule_attempt, int) or not isinstance(model, str) or not model:
            continue
        if rule_attempt <= attempt and (best_attempt is None or rule_attempt > best_attempt):
            best_attempt = rule_attempt
            best_model = model
    return best_model


def _from_split(split: object, task_id: str) -> str | None:
    if not isinstance(split, list):
        return None
    weighted: list[tuple[str, int]] = []
    for part in split:
        if not isinstance(part, dict):
            continue
        model = part.get("model")
        weight = part.get("weight")
        if isinstance(model, str) and model and isinstance(weight, int) and weight > 0:
            weighted.append((model, weight))
    total = sum(weight for _model, weight in weighted)
    if total <= 0:
        return None
    # sha256, not hash(): stable across processes and restarts.
    bucket = int.from_bytes(hashlib.sha256(task_id.encode()).digest()[:8], "big") % total
    for model, weight in weighted:
        if bucket < weight:
            return model
        bucket -= weight
    return None


def resolve_model(
    policy: dict | None, *, task_id: str, attempt: int, codex_model: str
) -> ModelChoice:
    if not isinstance(policy, dict):
        return _choice(codex_model, codex_model, "no policy")
    model = _from_rules(policy.get("rules"), attempt)
    if model:
        return _choice(model, codex_model, f"attempt rule for attempt {attempt}")
    model = _from_split(policy.get("split"), task_id)
    if model:
        return _choice(model, codex_model, "weighted split")
    default = policy.get("default_model")
    if isinstance(default, str) and default:
        return _choice(default, codex_model, "policy default")
    return _choice(codex_model, codex_model, "no applicable policy")


def budget_fallback(policy: dict | None) -> str | None:
    if not isinstance(policy, dict):
        return None
    model = policy.get("budget_fallback_model")
    return model if isinstance(model, str) and model else None
