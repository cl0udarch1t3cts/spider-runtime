# Spider Executor

Deterministic production runtime for [`spider-scripts`](https://github.com/cl0udarch1t3cts/spider-scripts). It persists registrations and execution work in MongoDB, runs provisioned scrapers without an LLM, validates provenance and expected fields, and stores production records in MongoDB.

Spider Doctor is invoked only at two boundaries:

- asynchronous registration creates a durable `create` task;
- a Doctor-eligible execution problem creates a durable `repair` task.

Normal successful execution never invokes Doctor or Codex.

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

## Asynchronous registration

Registration accepts exactly `entry_id`, `businessname`, and `address`. It persists the entry and deduplicated Doctor creation task before returning `202 Accepted`; it does not wait for Codex, tests, Git publication, or provisioning.

Registration is the only public entry-creation path; there is no public entry mutation endpoint. The prototype permits one active create-or-repair Doctor task per entry.

The executor resolves the current full `spider-scripts` Git commit through its injected release provider and stores that immutable SHA as the creation task's `base_release`; it is intentionally not accepted from the caller.

```bash
curl -i -X POST http://127.0.0.1:8000/api/v1/register \
  -H 'content-type: application/json' \
  -d '{
    "entry_id": "business-123",
    "businessname": "Example AG",
    "address": "Main Street 1, 8000 Zürich"
  }'
```

Representative response:

```json
{
  "entry_id": "business-123",
  "task_id": "doctor-task-id",
  "status": "queued",
  "operation": "create"
}
```

MongoDB is authoritative. Doctor claims the stored task and retrieves the business identity from the stored entry; the request does not contain a slug.

## Manual execution jobs

After a Doctor result has been provisioned, execution jobs use `entry_id`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/execution-jobs \
  -H 'content-type: application/json' \
  -d '{
    "entry_id": "business-123",
    "trigger": "manual",
    "idempotency_key": "demo:business-123:1"
  }'
```

The executor stores successful extracted records in MongoDB.

Manual enqueue returns `409 Conflict` until the entry has an activated scraper release. This initial prototype activates only one entry and fails closed if work targets another entry. Activation/release mismatches are control-plane failures and never create Doctor repair work.

## Doctor handoff

`MongoControlService.consume_doctor_handoff(task_id)` consumes a succeeded Doctor task whose `result.commit_sha` is a full 40-character Git SHA. It idempotently provisions that exact published commit outside the MongoDB transaction, then atomically updates the entry's `scraper_release`, creates one execution job pinned to that revision, and records the handoff job on the Doctor task. Re-consuming the same task returns the same scheduled job without provisioning or scheduling it again.

Provisioning refuses dirty checkouts, accepts an exact Doctor commit even when the remote branch has advanced, and never advances beyond the recorded SHA. Repair-task budget is stored on the entry so fresh tasks cannot reset it indefinitely; after two repair tasks, later deterministic failures enter `human_review_required`.

The API binds to localhost by default. Put TLS and authentication in front of it before exposing it beyond the host.

## Configuration

All settings use the `SPIDER_` prefix. Important values:

- `SPIDER_MONGODB_URI`
- `SPIDER_MONGODB_DATABASE`
- `SPIDER_SCRIPTS_ROOT`
- `SPIDER_ARTIFACT_ROOT`
- `SPIDER_WORKER_ID`
- `SPIDER_RUNNER_TIMEOUT_SECONDS`
- `SPIDER_RUNNER_URL`
