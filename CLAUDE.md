# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository layout

Monorepo for the spider platform runtime (merged from formerly standalone repos, full history preserved):

- `spider-executor/` — deterministic, **LLM-free** production runtime: registration API, MongoDB control plane, worker, sandboxed scraper runner.
- `spider-doctor/` — trusted dispatcher that creates/repairs scrapers by launching one disposable, stock Hermes (LLM) container per task.
- `docs/` — arc42 `ARCHITECTURE.md`, `OPERATIONS.md` (authoritative runbook), `VM_SETUP.md`, `TODO.md`.

The scrapers themselves live in the **separate sibling repo** `spider-scripts` (expected at `../spider-scripts` relative to this repo's root). The Doctor clones and commits into it; the Executor mounts it read-only (compose default `../../spider-scripts` from inside `spider-executor/`). Per-service agent rules exist in `spider-executor/AGENTS.md` and `spider-doctor/README.md` — read them before changing that service.

## Commands

Both services use `uv` (never system pip) and Python ≥3.12. Run commands from inside the service directory:

```bash
cd spider-executor   # or spider-doctor
uv sync --frozen --dev
uv run pytest                          # full suite
uv run pytest tests/test_service.py -q # one file
uv run pytest tests/test_service.py::test_name  # one test
uv run ruff check .                    # lint (CI-enforced for spider-doctor)
```

`spider-executor/scripts/mongo_smoke.py` is not a pytest test; it runs inside CI's compose stack against a real MongoDB replica set (see `.github/workflows/executor-test.yml`).

CI lives in root `.github/workflows/` (`doctor-test.yml`, `executor-test.yml`), path-filtered per service directory — a change under `spider-doctor/**` only triggers `doctor-test`.

The root `Makefile` wraps VM operations (start/stop/restart/update/logs for both compose stacks, in the runbook's required order); `make help` lists targets. It is for deployment, not development.

## Architecture

Full detail is statically imported from @docs/ARCHITECTURE.md — the load-bearing ideas:

**Two services, one hard boundary.** The Executor must stay deterministic — no LLM calls ever. All LLM work happens in Doctor's disposable task containers. Failure classification enforces this split: only deterministic scraper/schema/identity/semantic failures create `doctor_tasks`; network blocks and rate limits must not.

**MongoDB is the only durable state** (`spider` db, replica set `rs0`). Key collections: `entries`, jobs, execution runs/records, `doctor_tasks` (durable audit + recovery state — never `deleteMany`; the real error behind Doctor's generic "attempt failed" log line is in `doctor_tasks.last_error`), and `runtime_state`. Jobs are at-least-once; every side effect must be idempotent.

**Activation contract (single-entry prototype).** `runtime_state` doc `{_id: "activated_entry"}` holds the one entry/release pair allowed to run. `service.enqueue()` and the worker refuse anything else. The only writer is `consume_doctor_handoff()`, which activates the entry at the Doctor's published commit SHA and enqueues the handoff job. Tests seeding jobs must create this record (see `scripts/mongo_smoke.py`).

**Doctor pipeline** (worker.py → workspace.py → launcher.py → publisher.py): claim task with lease → fresh clone of `spider-scripts` at the pinned `base_release` → run disposable Hermes container → validate the diff against a strict allowlist (`scrapers/<entry_id>`, `tests/fixtures/<entry_id>`, `PROGRESS.md`, `registry.json`, `tests/verify.py`; untracked Hermes scratch files are discarded) → commit, persist `candidate_sha` in Mongo **before** push, rebase stale candidates onto the remote tip → mark `succeeded` only when the SHA is reachable from main. Tasks with a persisted `candidate_sha` are retried forever; tasks without one exhaust at `max_attempts`.

**Doctor security isolation.** Task containers get no credentials: provider traffic goes through the broker sidecar (holds the Codex OAuth, built from the exact pinned stock Hermes image), public HTTP through a restricted Squid egress proxy; only those two are dual-homed. Only the trusted dispatcher has the Docker socket, Git SSH identity, and Mongo access. Never point `SPIDER_DOCTOR_HERMES_DIGEST` at `:latest` or an unpinned image; OAuth lives only in `spider-doctor/data/broker-hermes/` and `data/` is never committed.

**Schema evolution** is ordered: the Executor's validation accepts undeclared null fields, so new record schema fields (e.g. JOBS) deploy dormant; entries pick them up on re-registration, which pins a fresh `spider-scripts` HEAD and regenerates the scraper.

## Conventions

- Strict RED-GREEN-REFACTOR TDD in `spider-executor`.
- A non-null extracted field must carry real-origin provenance; record the exact `spider-scripts` Git SHA used for every run.
- Deployment ordering matters: Executor must be up and healthy before Doctor starts (Doctor joins the `spider-executor_control` network). The compose stacks are deliberately separate projects — do not merge them; compose project names (`spider-executor`, `spider-doctor`) come from directory basenames and existing volumes/networks depend on them.
