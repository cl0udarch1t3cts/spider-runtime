# Spider Platform VM Setup Tutorial

This tutorial deploys the complete Spider platform on one Ubuntu VM:

- `spider-executor`: registration API and deterministic scraper runtime
- MongoDB: durable registrations, tasks, execution state, and scraped records
- Spider Doctor: creates and repairs deterministic scrapers with stock Hermes/Codex
- `spider-scripts`: authoritative scraper source repository
- `docs/` (in `spider-runtime`): architecture, operations, and bulk-registration commands

The commands assume:

- VM user: `spider`
- project root: `/home/spider/projects`
- Ubuntu 26.04 or a compatible Ubuntu release
- Docker Engine and Docker Compose are already installed by the VM administrator
- the `spider` user can run Docker without `sudo`
- GitHub SSH access is configured for `cl0udarch1t3cts`

Do each step in order. Do not continue until its verification command passes.

After installation, use [`OPERATIONS.md`](OPERATIONS.md) for routine start, stop, restart, update, monitoring, backup, and incident procedures.

---

## 0. Important operating rules

1. Run deployment commands as `spider`, not as `root`.
2. Never put OAuth credentials in `.env`, `data/hermes`, a task home, or Git.
3. OAuth belongs only in `spider-doctor/data/broker-hermes`.
4. Never use an unpinned Hermes image or `:latest`.
5. Start `spider-executor` before Spider Doctor because Doctor joins Executor's control network.
6. Keep the sibling `spider-scripts` checkout clean. Doctor publishes through isolated workspaces and Git.
7. Do not use `db.doctor_tasks.deleteMany({})`. Task records are the durable audit and recovery state.
8. Do not manually change a running/queued task unless the recovery procedure explicitly requires it.
9. Registration uses the exact `entry_id`; no slug is generated or required.

---

## 1. Verify the VM identity

```bash
whoami
hostname
pwd
```

Expected user:

```text
spider
```

Create and enter the project directory:

```bash
mkdir -p /home/spider/projects
cd /home/spider/projects
```

Verify:

```bash
pwd
```

Expected:

```text
/home/spider/projects
```

> Keep development checkouts on other machines separate. Before any production Git or Docker command, confirm the prompt says `spider@spider-01` and the path begins with `/home/spider/projects`.

---

## 2. Verify Docker access

```bash
docker version
docker compose version
docker run --rm hello-world
```

Also verify the socket is accessible and note its group:

```bash
id
stat -c 'docker socket owner=%u:%g mode=%a' /var/run/docker.sock
```

All commands must work without `sudo`. If they fail, stop here and have the VM administrator add `spider` to the Docker group, then sign out and back in.

---

## 3. Verify GitHub SSH access

```bash
ssh -T git@github.com
```

A successful response identifies the GitHub account even though GitHub does not provide shell access.

Verify the SSH files are private:

```bash
stat -c '%a %n' ~/.ssh ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.pub
```

Typical safe modes are `700` for `~/.ssh` and `600` for the private key.

Do not continue until this works. Doctor uses this read-only SSH identity to publish validated commits to `spider-scripts`.

---

## 4. Clone the two repositories

`spider-runtime` is the monorepo containing `spider-doctor/`, `spider-executor/`,
and its `docs/`. `spider-scripts` stays a standalone repository because the
Doctor clones and commits into it.

```bash
cd /home/spider/projects

git clone git@github.com:cl0udarch1t3cts/spider-scripts.git
git clone git@github.com:cl0udarch1t3cts/spider-runtime.git
```

Verify all checkouts:

```bash
for repo in spider-scripts spider-runtime; do
  git -C "/home/spider/projects/$repo" status --short --branch
done
```

Each repository should be on `main` and clean.

Verify `spider-scripts` can see its remote:

```bash
git -C /home/spider/projects/spider-scripts remote -v
git -C /home/spider/projects/spider-scripts fetch --no-tags origin main
```

---

## 5. Start Spider Executor and MongoDB

The Executor Compose stack includes:

- MongoDB replica set
- one-shot `mongo-init`
- registration API bound to `127.0.0.1:8000`
- deterministic worker
- isolated scraper runner

The repository override pins MongoDB to `7.0.40` for the production VM kernel compatibility requirement.

```bash
cd /home/spider/projects/spider-runtime/spider-executor
docker compose up --build -d
```

Wait for readiness:

```bash
curl --fail-with-body http://127.0.0.1:8000/health/ready
```

Inspect services:

```bash
docker compose ps -a
```

Expected:

- `mongo`: up and healthy
- `api`: up
- `worker`: up
- `runner`: up and healthy
- `mongo-init`: exited with status `0` (this is normal)

Verify the control network exists:

```bash
docker network inspect spider-executor_control --format '{{.Name}} internal={{.Internal}}'
```

Expected name:

```text
spider-executor_control
```

If the health check fails, inspect only the recent Executor logs:

```bash
docker compose logs --no-color --since=10m mongo mongo-init api worker runner
```

Do not start Doctor until Executor is healthy.

---

## 6. Generate Doctor's non-secret `.env`

```bash
cd /home/spider/projects/spider-runtime/spider-doctor
./scripts/init-env.py
```

This calculates:

- absolute Doctor and `spider-scripts` host paths
- the `spider` UID/GID
- Docker socket group ID
- the reviewed stock-Hermes digest
- network and publication settings

Verify the file exists with mode `600`:

```bash
stat -c '%a %n' .env
grep '^SPIDER_DOCTOR_HERMES_DIGEST=sha256:[0-9a-f]\{64\}$' .env
```

Expected mode:

```text
600 .env
```

The digest is a setting, not a secret. Never substitute `latest` or an unreviewed image.

If `.env` already exists, do not overwrite it blindly. Back it up and compare first:

```bash
cp .env /tmp/spider-doctor.env.backup
diff -u .env.example .env || true
```

Use `./scripts/init-env.py --force` only after reviewing the backup and confirming the checkout path is `/home/spider/projects/spider-runtime/spider-doctor`.

---

## 7. Configure the credential-free task home and trusted OAuth home

Run this only during first setup or an intentional Hermes-home reseed:

```bash
cd /home/spider/projects/spider-runtime/spider-doctor
./scripts/configure-hermes.sh
```

The script will:

1. create a random mode-`0600` task-to-broker token;
2. regenerate `data/hermes/config.yaml` from the pinned stock image;
3. configure the local Doctor broker provider;
4. verify the credential-free task configuration;
5. interactively open stock Hermes Codex OAuth if broker OAuth is absent.

Complete the OAuth flow when prompted.

Verify credential placement without displaying secrets:

```bash
test -s data/broker-hermes/auth.json && echo 'broker OAuth present'
test ! -s data/hermes/auth.json && echo 'task home has no OAuth'
test ! -s data/hermes/.env && echo 'task home has no secret env'
stat -c '%a %n' data/proxy-token
```

Expected:

```text
broker OAuth present
task home has no OAuth
task home has no secret env
600 data/proxy-token
```

Do not copy `data/broker-hermes/auth.json` into another directory. Do not commit anything under `data/`.

### Why `configure-hermes.sh` should not be rerun casually

The task seed is deployment-generated. The script intentionally removes its old `config.yaml` and asks the current pinned stock image to seed the current schema before applying settings. This prevents an obsolete deployment config from being carried forever. It does not touch broker OAuth unless OAuth is missing.

---

## 8. Start Spider Doctor

```bash
cd /home/spider/projects/spider-runtime/spider-doctor
./scripts/start.sh
```

`start.sh` performs these operations in order:

1. builds and starts the restricted egress proxy;
2. creates/attests the internal task network;
3. runs fail-closed deployment preflight;
4. builds Doctor and the stock-Hermes broker sidecar;
5. starts all services and waits for health checks.

The final output should contain:

```text
PASS: Doctor deployment preflight succeeded
PASS: disposable tasks have no direct route; public HTTP(S) uses the restricted proxy
```

Verify services:

```bash
docker compose ps -a
```

Expected:

- `broker`: healthy
- `doctor`: up
- `egress-proxy`: up/healthy

Inspect recent logs:

```bash
docker compose logs --no-color --since=10m doctor broker egress-proxy
```

A Squid `netdb.state` permission warning can be nonblocking. Public HTTPS must show `TCP_TUNNEL/200`, not blanket `TCP_DENIED/403`.

---

## 9. Run a single-entry canary

Start with one real business before submitting the bulk TODO list.

```bash
curl --fail-with-body -sS \
  -X POST http://127.0.0.1:8000/api/v1/register \
  -H 'content-type: application/json' \
  --data-binary @- <<'JSON'
{
  "entry_id": "MwSzyU-pjR5VxWMHNXDG4A",
  "businessname": "Restaurant Tschingg am Stauffacher",
  "address": "Lutherstrasse 4, 8004 Zürich"
}
JSON
```

Expected response fields:

```json
{
  "entry_id": "MwSzyU-pjR5VxWMHNXDG4A",
  "task_id": "<generated UUID>",
  "status": "queued",
  "operation": "create"
}
```

Save the returned `task_id`.

---

## 10. Monitor task progress

### Find active disposable task containers

```bash
docker ps \
  --filter 'label=spider-doctor.managed=true' \
  --format 'table {{.Names}}\t{{.Status}}'
```

For one task:

```bash
docker ps \
  --filter 'label=spider-doctor.task-id=TASK_ID' \
  --format 'table {{.Names}}\t{{.Status}}'
```

Replace `TASK_ID` exactly.

### Follow the active task's logs

```bash
container_id=$(docker ps -q --filter 'label=spider-doctor.task-id=TASK_ID')
if [ -n "$container_id" ]; then
  docker logs -f "$container_id"
else
  echo 'No active disposable container; query MongoDB for final state.'
fi
```

Press `Ctrl+C` to stop watching logs. This does not stop the task.

Hermes one-shot mode may remain quiet between bootstrap and completion. Network activity can be observed with:

```bash
docker compose logs -f egress-proxy
```

### Query durable task state

```bash
docker exec spider-executor-mongo-1 mongosh --quiet spider --eval '
db.doctor_tasks.find(
  {_id:"TASK_ID"},
  {_id:1,entry_id:1,status:1,attempts:1,max_attempts:1,lease:1,candidate_sha:1,result:1,last_error:1}
).forEach(printjson)
'
```

Lifecycle:

```text
queued -> running -> candidate persisted -> pushed -> succeeded
                 \-> queued for bounded retry
                 \-> exhausted
```

An old `last_error` can remain visible while a later attempt is running. Use `status`, `attempts`, `lease`, and the active task container together.

---

## 11. Verify publication and Executor handoff

A successful Doctor task contains:

- `status: succeeded`
- `candidate_sha`
- `result.commit_sha`

Doctor writes changes in an isolated workspace, validates the real Git diff, commits only allowlisted files, persists the candidate SHA, pushes that exact commit to `spider-scripts/main`, and verifies the remote branch contains it.

The sibling checkout does not automatically move. Update it only when clean:

```bash
cd /home/spider/projects/spider-scripts
git status --short --branch
git pull --ff-only
```

Verify the entry files:

```bash
test -f scrapers/ENTRY_ID/meta.json
test -f scrapers/ENTRY_ID/scrape.py
git log -1 --oneline -- scrapers/ENTRY_ID
```

Executor then consumes the succeeded Doctor handoff, provisions the exact commit, runs the deterministic scraper, and stores production output in MongoDB.

---

## 12. Use the bulk registration TODO

After the canary succeeds, open:

```text
/home/spider/projects/spider-runtime/docs/TODO.md
```

Each checklist item contains a shell-safe `curl` using a quoted JSON heredoc. Run one request at a time initially and verify the returned task ID before moving to a larger batch.

Some source IDs in the supplied list contain spaces or begin with `_`/`-`. `EXAMPLES.md` preserves them exactly and marks them with a warning. The registration API is expected to reject those IDs until the source value is corrected. Do not silently “repair” an identifier.

---

## 13. Safe update procedure

### Update Executor

```bash
cd /home/spider/projects/spider-runtime/spider-executor
git status --short --branch
git pull --ff-only
docker compose up --build -d
curl --fail-with-body http://127.0.0.1:8000/health/ready
```

### Update Doctor without wasting an active attempt

First check for running tasks:

```bash
docker ps --filter 'label=spider-doctor.managed=true' --format '{{.Names}} {{.Status}}'
```

If no task is running:

```bash
cd /home/spider/projects/spider-runtime/spider-doctor
git status --short --branch
git pull --ff-only
./scripts/start.sh
```

If a task is running, let it finish unless there is a confirmed infrastructure defect that will consume the attempt. To preserve a queued retry while diagnosing infrastructure:

```bash
docker compose stop doctor
```

Do not stop a healthy disposable task casually. Do not manually edit the Mongo lease.

---

## 14. Recovery patterns learned during deployment

### `cd: can't cd to /opt/data`

Cause: stock Hermes bootstrap needed the narrow `DAC_READ_SEARCH` capability after all ambient capabilities were dropped and the task home was mode `0700`.

Current launcher includes only the reviewed capability allowlist. Verify the deployed task command through tests and do not grant broad `DAC_OVERRIDE`.

### All HTTPS requests show `TCP_DENIED/403`

Cause: Squid rejected `CONNECT` before applying its port and destination restrictions.

Current policy permits `CONNECT` only to port `443` and still blocks private, loopback, link-local, metadata, multicast, and internal destinations. Healthy public requests show `TCP_TUNNEL/200`.

### `Hermes Doctor exceeded task storage limits`

Cause: uv populated hundreds of megabytes and thousands of files under the persistent task home cache.

Current launcher redirects uv, pip, and XDG caches into bounded, non-executable `/tmp` tmpfs. Persistent limits remain enforced.

Diagnose a task:

```bash
cd /home/spider/projects/spider-runtime/spider-doctor
./scripts/diagnose-task-storage.sh TASK_ID
```

### Agent returns `status: succeeded`

Cause: the generated schema previously exposed trusted host-only status values.

Current schema lets the agent return only `awaiting_review` or `failed`. Only trusted Doctor code can mark a task succeeded after validation and publication.

### Agent returns `/workspace/...` changed paths

Current parser safely removes only the exact `/workspace/` mount prefix and continues to reject every other absolute path and any `..` traversal. Trusted code independently computes the actual Git changes before publication.

### `No user exists for uid 1000` during Git publication

Cause: Doctor ran with the host numeric UID but the container had no matching passwd identity, causing OpenSSH to fail.

Current Doctor image creates a `doctor` user/group at the configured deployment UID/GID during build.

If a `candidate_sha` is already persisted, restarting Doctor resumes publication without regenerating the scraper.

### Rapid repeated `Doctor attempt status=failed` messages

Stop the dispatcher immediately:

```bash
docker compose stop doctor
```

Then list recent exact errors:

```bash
docker exec spider-executor-mongo-1 mongosh --quiet spider --eval '
db.doctor_tasks.find(
  {},
  {_id:1,entry_id:1,status:1,attempts:1,max_attempts:1,updated_at:1,candidate_sha:1,last_error:1}
).sort({updated_at:-1}).limit(20).forEach(printjson)
'
```

Do not diagnose from the generic summary line alone.

### `git pull` reports local changes

Confirm the host and path first:

```bash
hostname
pwd
git status --short --branch
```

Never reset, clean, or stash unfamiliar source changes. Development and production machines can have similarly named checkouts.

### Compose says `SPIDER_DOCTOR_HERMES_DIGEST` is missing

Verify the production `.env`:

```bash
grep '^SPIDER_DOCTOR_HERMES_DIGEST=sha256:[0-9a-f]\{64\}$' .env
```

If missing, recover from a reviewed `.env` backup or regenerate machine settings only after confirming the production host/path. Never invent a digest.

---

## 15. Routine health checklist

```bash
# Executor
cd /home/spider/projects/spider-runtime/spider-executor
docker compose ps -a
curl --fail-with-body http://127.0.0.1:8000/health/ready

# Doctor
cd /home/spider/projects/spider-runtime/spider-doctor
docker compose ps -a
python3 scripts/preflight.py

# Repositories
for repo in spider-scripts spider-runtime; do
  git -C "/home/spider/projects/$repo" status --short --branch
done
```

Healthy state:

- Executor API responds on localhost
- MongoDB and runner are healthy
- Doctor broker is healthy
- Doctor dispatcher is up
- restricted egress preflight passes
- `spider-scripts` is clean
- no unexpected managed task containers remain after tasks finish
- OAuth exists only in `spider-doctor/data/broker-hermes`

---

## 16. Backup priorities

Back up:

1. Docker volume containing MongoDB data
2. `spider-doctor/data/broker-hermes` OAuth state (securely, never in Git)
3. `spider-doctor/data/tasks` and `data/workspaces` while recovering persisted candidates
4. Git repositories/remotes, especially `spider-scripts`

Do not treat disposable Hermes task homes or package caches as authoritative business data.

The authoritative durable boundaries are:

- MongoDB for registrations, tasks, execution state, and scraped records
- GitHub `spider-scripts` for scraper source and published commit history
