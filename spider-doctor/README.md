# Spider Doctor

A trusted dispatcher that consumes `spider.doctor_tasks` and launches one disposable, stock Hermes container per creation or repair attempt. `spider-executor` remains deterministic and LLM-free.

## Security boundary

The disposable Hermes task receives only:

- a task-specific clone of `spider-scripts` at the authoritative release SHA;
- task-scoped Mongo evidence serialized to a read-only JSON file;
- a task result directory;
- a dedicated, credential-free Hermes home;
- a narrow client token accepted only by the local broker.

It does **not** receive MongoDB credentials, the broker's OAuth credential, GitHub credentials, production artifacts, or `/var/run/docker.sock`. The unmodified stock image briefly uses only `CHOWN`, `SETUID`, and `SETGID` to map its runtime user to the host UID/GID, then executes Hermes as that non-root user. Its writable container layer is disposable under `--rm`; only task-scoped mounts persist. It is resource-limited and attached to an internal Docker network with no direct external route.

Public HTTP(S) from a task must traverse the restricted Squid sidecar, which rejects private, loopback, link-local, metadata, multicast, and other non-public destinations after DNS resolution. Provider traffic goes to the local stock-Hermes broker. Only the trusted broker and restricted proxy are dual-homed; the task is not.

The trusted Doctor container alone receives the Docker socket, Mongo control-network access, a read-only `spider-scripts` source checkout, persistent task workspaces, and the host's Git SSH identity. It validates the actual diff before host-side commit and publication from the isolated workspace.

After verification, trusted code stages only allowlisted paths, creates a commit, persists its candidate SHA in MongoDB **before** push, and marks the task `succeeded` only after that SHA is reachable from the publication branch. Restart reconciliation republishes the durable candidate without regenerating code and records it as `result.commit_sha`.

## Containerized deployment

Hermes is not installed on the VM. Disposable task agents use the official stock image pinned in `.env.example`. The broker sidecar builds **from that exact stock image** and adds only the project-owned restricted HTTP entrypoint; it does not patch or fork Hermes. The sidecar reuses the stock image's tested Codex OAuth resolver and refresh logic while keeping the OAuth store outside every task container. The Doctor dispatcher and restricted egress proxy have separate project-owned images.

Prerequisites:

- Docker Engine with Compose;
- `spider-executor` running from the sibling checkout, including its `spider-executor_control` network;
- a clean sibling `spider-scripts` checkout with a writable GitHub remote;
- the deployment user authorized for Docker and GitHub SSH pushes.

Never use `:latest`; mutable Hermes references are rejected.

### 1. Generate non-secret deployment settings

```bash
./scripts/init-env.py
```

This writes `.env` with the current absolute paths, user/group IDs, Docker socket group, and the reviewed stock-Hermes digest. `.env` contains settings, not OAuth credentials or broker tokens.

### 2. Configure the two Hermes homes

```bash
./scripts/configure-hermes.sh
```

The script:

- creates a random mode-`0600` client token;
- configures `data/hermes` as the credential-free disposable-task home;
- configures its provider endpoint as `http://spider-doctor-broker:8645/v1`;
- interactively performs `openai-codex` OAuth only in `data/broker-hermes`.

The OAuth credential is never copied into `data/hermes`, `.env`, or a task mount. The legacy `sandbox/` and `data/codex/` layout is ignored and not used.

### 3. Start and verify

```bash
./scripts/start.sh
```

Startup creates the internal task network and its restricted proxy/broker gateways, runs fail-closed preflight checks, builds the Doctor image, and starts the continuous dispatcher.

```bash
docker compose ps -a
docker compose logs --no-color --tail=100 doctor broker egress-proxy
```

`mongo-init` belongs to the Executor stack and is expected to remain exited with status 0.

### Update or restart

```bash
git pull --ff-only
./scripts/start.sh
```

Compose rebuilds changed project images and recreates services as needed. Runtime and OAuth data are bind-mounted under ignored `data/` and survive container replacement.

To stop Doctor without deleting runtime data:

```bash
docker compose down
```

## Task lifecycle

Creation and repair tasks are written by `spider-executor`. Doctor consumes the authoritative `entry_id`, `base_release`, entry record, and source run record from MongoDB.

```text
queued -> running (lease token + attempt)
       -> candidate SHA persisted -> pushed -> succeeded(result.commit_sha)
       -> queued (bounded retry after operational failure)
       -> exhausted (attempt budget consumed)
```

Completion and failure transitions require the current lease token. A persisted candidate remains reclaimable after lease expiry or process restart, including after the generation attempt budget is consumed.

## Development verification

```bash
uv sync --frozen --dev
uv run pytest
uv run ruff check src tests scripts
```
