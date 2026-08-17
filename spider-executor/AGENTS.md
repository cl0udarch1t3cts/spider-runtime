# Spider Executor operating rules

This repository is the deterministic production runtime for `spider-scripts`.

## Invariants

- No LLM calls belong in this service.
- A non-null extracted field must have real-origin provenance.
- Network/rate-limit/datacenter blocking must not create Script Doctor work.
- Only deterministic scraper, schema, identity, or semantic failures are doctor eligible.
- Jobs are at-least-once and every side effect must be idempotent.
- Scraper source stays in `cl0udarch1t3cts/spider-scripts`; record the exact Git SHA used.
- Runtime artifacts use relative keys under the configured artifact root.

## Development

Use `uv`, never system pip. Follow strict RED-GREEN-REFACTOR TDD.

```bash
uv sync --dev
uv run pytest
```

## Local integration

`docker compose up --build` starts a single-node MongoDB replica set, API and worker.
The adjacent `../spider-scripts` checkout is mounted read-only.
