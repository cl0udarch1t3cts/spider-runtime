from spider_doctor.model_policy import budget_fallback, resolve_model

CODEX = "gpt-5.4"


def test_no_policy_resolves_to_the_codex_model() -> None:
    choice = resolve_model(None, task_id="t-1", attempt=1, codex_model=CODEX)

    assert choice.model == CODEX
    assert choice.provider == "doctor-codex"
    assert choice.budget_gated is True


def test_attempt_rules_pick_the_highest_matching_attempt() -> None:
    policy = {
        "rules": [
            {"attempt": 1, "model": "qwen3-coder:free"},
            {"attempt": 2, "model": CODEX},
        ]
    }

    first = resolve_model(policy, task_id="t-1", attempt=1, codex_model=CODEX)
    second = resolve_model(policy, task_id="t-1", attempt=2, codex_model=CODEX)
    third = resolve_model(policy, task_id="t-1", attempt=3, codex_model=CODEX)

    assert first.model == "qwen3-coder:free"
    assert first.provider == "doctor-openrouter"
    assert first.budget_gated is False
    assert second.model == CODEX
    # Attempts beyond the last rule keep using the last rule.
    assert third.model == CODEX


def test_split_policy_is_deterministic_per_task() -> None:
    policy = {
        "split": [
            {"model": CODEX, "weight": 50},
            {"model": "qwen3-coder:free", "weight": 50},
        ]
    }

    choices = {
        task_id: resolve_model(policy, task_id=task_id, attempt=1, codex_model=CODEX).model
        for task_id in (f"task-{n}" for n in range(40))
    }

    # Same task id always resolves identically.
    for task_id, model in choices.items():
        again = resolve_model(policy, task_id=task_id, attempt=1, codex_model=CODEX)
        assert again.model == model
    # Both sides of the split are actually used.
    assert set(choices.values()) == {CODEX, "qwen3-coder:free"}


def test_malformed_policy_falls_back_to_default_then_codex() -> None:
    garbage = {"rules": "nope", "split": 7, "default_model": "deepseek-r1:free"}

    choice = resolve_model(garbage, task_id="t-1", attempt=1, codex_model=CODEX)
    assert choice.model == "deepseek-r1:free"

    fully_broken = {"rules": [{"attempt": "x"}]}
    assert (
        resolve_model(fully_broken, task_id="t-1", attempt=1, codex_model=CODEX).model
        == CODEX
    )


def test_budget_fallback_accessor() -> None:
    assert budget_fallback({"budget_fallback_model": "deepseek-r1:free"}) == "deepseek-r1:free"
    assert budget_fallback({"budget_fallback_model": ""}) is None
    assert budget_fallback({}) is None
    assert budget_fallback(None) is None
