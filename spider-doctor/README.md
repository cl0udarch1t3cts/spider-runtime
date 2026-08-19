# Spider Doctor

A trusted host dispatcher that claims deterministic repair tasks from `spider.doctor_tasks` and launches **one disposable Hermes container per attempt**. The deterministic executor remains LLM-free.

## Security boundary

The Hermes container receives only:

- a standalone disposable clone of `spider-scripts` at the exact failing Git SHA;
- task-scoped Mongo evidence serialized to a read-only JSON file;
- a task result directory;
- a dedicated Hermes data directory.

It does **not** receive MongoDB credentials, production artifacts, GitHub credentials, or `/var/run/docker.sock`. It is non-root, capability-free, read-only except for the task mounts, resource-limited, and attached only to a named egress network. The dispatcher validates the actual Git diff and rejects changes outside the `entry_id`-specific allowlist.

After the disposable agent returns a verified patch, the trusted host dispatcher stages only the validated paths, commits, persists the candidate SHA in MongoDB, and pushes it. The task becomes `succeeded` only after the candidate is reachable from the configured publication branch. A crash or ambiguous push is reconciled from the durable candidate SHA without regenerating code.

## Prerequisites

- Docker Engine and the Docker CLI on the dispatcher host.
- A clean local `../spider-scripts` clone containing the failing release.
- MongoDB access from the dispatcher host.
- A dedicated Hermes home initialized for the Doctor.
- A pinned Hermes image reference such as `nousresearch/hermes-agent@sha256:<64 hex>`.
- A Docker network named `spider-doctor-egress` whose host firewall denies host, RFC1918, link-local, metadata, Mongo, and control-plane destinations. After independently verifying that enforcement, label it `spider-doctor.egress-policy=restricted-v1`; the launcher refuses an absent or unlabeled network. The label is an operator attestation, not a substitute for the firewall itself.

Never use `:latest` in production; mutable image references are rejected.

## Initialize the dedicated Hermes home

Create the home with the official image and configure its model/provider to use a credential-injecting proxy reachable on `spider-doctor-egress`:

```bash
mkdir -p data/hermes
docker run -it --rm \
  -v "$PWD/data/hermes:/opt/data" \
  nousresearch/hermes-agent@sha256:<digest> setup
```

Do **not** save a provider API key or OAuth credential during this setup. The launcher rejects a non-empty `.env` or `auth.json` in the seed home. The proxy must authenticate the task container without exposing its upstream provider credential to Hermes or scraper subprocesses, while independently enforcing model, budget, rate, and expiry policy.

The disposable clone's `AGENTS.md` is loaded automatically because Hermes starts in `/workspace`; it is the authoritative creation/repair procedure. An optional dedicated `spider-doctor` skill may add orchestration guidance, but the worker does not depend on an unverified skill installation.

## Configure

```bash
export SPIDER_DOCTOR_HERMES_IMAGE='nousresearch/hermes-agent@sha256:<digest>'
export SPIDER_DOCTOR_MONGODB_URI='mongodb://127.0.0.1:27017/spider?replicaSet=rs0&directConnection=true'
export SPIDER_DOCTOR_SOURCE_REPOSITORY='../spider-scripts'
export SPIDER_DOCTOR_HERMES_HOME='./data/hermes'
export SPIDER_DOCTOR_PROXY_TOKEN_FILE='./data/proxy-token'
```

All settings use the `SPIDER_DOCTOR_` prefix. See `src/spider_doctor/settings.py` for bounded defaults.

### Subscription broker configuration

The Doctor may receive a scoped local broker token, but never the provider's
OAuth credential. Create the token file as the Doctor user and keep it mode
`0600`:

```bash
mkdir -p data
openssl rand -hex 32 > data/proxy-token
chmod 600 data/proxy-token
```

Configure the dedicated, credential-free Hermes home through the Hermes CLI.
Replace `172.30.0.1` with the restricted Doctor bridge gateway that runs the
credential broker:

```bash
export HERMES_HOME="$PWD/data/hermes"
hermes config set providers.doctor-codex.api http://172.30.0.1:8645/v1
hermes config set providers.doctor-codex.transport codex_responses
hermes config set providers.doctor-codex.key_cmd 'cat /task/proxy-token'
hermes config set providers.doctor-codex.default_model gpt-5.4
hermes config set model.provider custom:doctor-codex
hermes config set model.default gpt-5.4
hermes config check
```

The dispatcher validates the host token file and mounts it read-only at
`/task/proxy-token`. The token is intentionally usable only against the
network-restricted local broker; the reusable OAuth access and refresh tokens
remain outside every disposable Doctor container.

Run the broker from a separate trusted Hermes home that contains the operator's
Codex OAuth login. Do not point it at `data/hermes`, which is intentionally
credential-free:

```bash
HERMES_HOME=/home/spider/.hermes hermes proxy start \
  --provider openai-codex \
  --host 172.30.0.1 \
  --client-token-file "$PWD/data/proxy-token" \
  --allowed-model gpt-5.4 \
  --requests-per-minute 20 \
  --max-concurrent-requests 2
```

Bind to the Doctor bridge gateway, not `0.0.0.0`, and enforce the restricted
network/firewall policy before applying the required network attestation label.

## Run

Creation and repair tasks are written by `spider-executor`. Doctor reads the authoritative `entry_id`, business identity, base release, and failure evidence from MongoDB; there is no separate enqueue command or slug contract.

Run one attempt or the continuous dispatcher:

```bash
uv sync --frozen --dev
uv run spider-doctor-worker --once
uv run spider-doctor-worker
```

## Task lifecycle

```text
queued -> running (lease token + attempt)
       -> candidate SHA persisted -> pushed -> succeeded
       -> queued (bounded retry after operational failure)
       -> exhausted (attempt budget consumed)
```

Completion and failure transitions require the current lease token. Expired final attempts become exhausted. Existing executor revisions must populate `priority`, `attempts`, `max_attempts`, `available_at`, and `lease` when creating Doctor tasks.

## Tests

```bash
uv run pytest
```

The test suite covers atomic leasing, stale completion fencing, retry/exhaustion, scoped Mongo evidence, pinned images, hardened Docker arguments, bounded process output, timeout cleanup, exact-SHA workspaces, path allowlisting, and worker completion.
