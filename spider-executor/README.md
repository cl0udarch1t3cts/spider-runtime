# Spider Executor

Deterministic production runtime for [`spider-scripts`](https://github.com/cl0udarch1t3cts/spider-scripts). It schedules and leases jobs through MongoDB, runs a pinned scraper checkout without an LLM, validates provenance and expected fields, stores historical records, and creates Script Doctor tasks only for deterministic failures. Scraper code runs in a separate read-only, resource-limited runner container with no MongoDB credentials or production artifact mount.

## Local development

```bash
uv sync --dev
uv run pytest
```

## Docker Compose vertical slice

Prerequisite: `spider-scripts` is checked out next to this repository.

```bash
docker compose up --build -d
curl http://127.0.0.1:8000/health/ready
```

Register an entry and schedule it:

```bash
curl -X PUT http://127.0.0.1:8000/api/v1/entries/dory-und-du-baden   -H 'content-type: application/json'   -d '{"name":"DORY & DU","website":"https://doryunddu.ch","scraper_release":"a96ce24c9028669507e83d1341989ede9190afe1","validation":{"required_fields":["NAME","EMAIL","PHONE_NUMBER"],"allowed_null_fields":["MENU"],"minimum_non_null_fields":6,"allowed_source_hosts":["doryunddu.ch","www.doryunddu.ch"]}}'

curl -X POST http://127.0.0.1:8000/api/v1/execution-jobs   -H 'content-type: application/json'   -d '{"slug":"dory-und-du-baden","trigger":"manual","idempotency_key":"demo:dory:1"}'
```

The API binds to localhost by default. Put TLS/authentication in front of it before exposing it beyond the host.

## Configuration

All settings use the `SPIDER_` prefix. Important values:

- `SPIDER_MONGODB_URI`
- `SPIDER_MONGODB_DATABASE`
- `SPIDER_SCRIPTS_ROOT`
- `SPIDER_ARTIFACT_ROOT`
- `SPIDER_WORKER_ID`
- `SPIDER_RUNNER_TIMEOUT_SECONDS`
- `SPIDER_RUNNER_URL`
