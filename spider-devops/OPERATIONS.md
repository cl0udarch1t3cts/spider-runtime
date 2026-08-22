# Spider Platform Operations Runbook

This runbook covers routine operation of the complete production platform on `spider-01`:

- MongoDB
- Spider Executor API
- Spider Executor worker
- isolated deterministic runner
- Spider Doctor dispatcher
- stock-Hermes/Codex broker
- restricted Doctor egress proxy
- disposable Doctor task containers

Initial machine installation and credential setup remain in [`VM_SETUP.md`](VM_SETUP.md).

## Assumptions

```text
Host: spider-01
User: spider
Project root: /home/spider/projects
Executor: /home/spider/projects/spider-executor
Doctor: /home/spider/projects/spider-doctor
Scrapers: /home/spider/projects/spider-scripts
Operations: /home/spider/projects/spider-devops
```

Run Docker commands as `spider`, without `sudo`.

## Safety rules

1. Start Executor before Doctor. Doctor depends on MongoDB and the external `spider-executor_control` network.
2. Stop Doctor before maintenance that could disrupt MongoDB, Git publication, networking, or Executor handoff.
3. Never delete MongoDB volumes to fix a startup problem.
4. Never run `db.doctor_tasks.deleteMany({})`.
5. Never manually alter a task until its exact durable state has been inspected.
6. Never re-register a failed entry merely to manufacture a retry. Corrected registration details may be posted under the same `entry_id` only while its create task is queued.
7. Never reset, clean, or force-update a checkout containing unfamiliar changes.
8. Keep OAuth only in `spider-doctor/data/broker-hermes`.
9. Keep management ports on host loopback:
   - Executor API: `127.0.0.1:8000`
   - MongoDB: `127.0.0.1:27017`
10. `mongo-init` and `runtime-init` are one-shot services. `Exited (0)` is healthy for them.

---

# 1. Quick status of the complete platform

Use plain `docker ps` to see containers from every Compose project, regardless of the current directory:

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Include stopped and one-shot containers:

```bash
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Executor status:

```bash
cd /home/spider/projects/spider-executor
docker compose ps -a
curl --fail-with-body http://127.0.0.1:8000/health/ready
```

Expected Executor state:

- `mongo`: `Up ... (healthy)`
- `mongo-init`: `Exited (0)`
- `runtime-init`: `Exited (0)`
- `runner`: `Up ... (healthy)`
- `api`: `Up`
- `worker`: `Up`
- readiness response: `{"status":"ok"}`

Doctor status:

```bash
cd /home/spider/projects/spider-doctor
docker compose ps -a
```

Expected Doctor state:

- `egress-proxy`: `Up`
- `broker`: `Up ... (healthy)`
- `doctor`: `Up`

Check localhost listeners:

```bash
ss -ltn | grep -E '127\.0\.0\.1:(8000|27017)'
```

---

# 2. Start the full platform

## Normal full start

Start Executor first:

```bash
cd /home/spider/projects/spider-executor
docker compose up -d --wait --wait-timeout 180
curl --fail-with-body http://127.0.0.1:8000/health/ready
```

Then start Doctor through its reviewed launcher and preflight:

```bash
cd /home/spider/projects/spider-doctor
./scripts/start.sh
```

Final verification:

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

## Start after a VM reboot

The long-running services use `restart: unless-stopped`, but verify them explicitly after every reboot:

```bash
cd /home/spider/projects/spider-executor
docker compose up -d --wait --wait-timeout 180
curl --fail-with-body http://127.0.0.1:8000/health/ready

cd /home/spider/projects/spider-doctor
./scripts/start.sh
```

Do not assume Doctor is processing tasks merely because its broker and proxy are up; verify the `doctor` service itself.

## Start only Doctor after it was intentionally stopped

Use this only when Executor is already healthy and Doctor’s broker/proxy are already present:

```bash
cd /home/spider/projects/spider-doctor
docker compose start doctor
docker compose ps doctor
```

If the Doctor container does not exist, dependencies changed, or preflight has not run, use:

```bash
./scripts/start.sh
```

---

# 3. Stop the platform

## Stop Doctor processing only

This preserves queued tasks and leaves broker/proxy available:

```bash
cd /home/spider/projects/spider-doctor
docker compose stop doctor
docker compose ps doctor
```

Use this before diagnosing repeated Doctor failures or before maintenance.

## Stop the complete Doctor stack

```bash
cd /home/spider/projects/spider-doctor
docker compose stop
```

This stops Doctor, broker, and egress proxy without removing containers or data.

## Stop Executor application processing but leave MongoDB running

Stop Doctor first, then:

```bash
cd /home/spider/projects/spider-executor
docker compose stop worker api runner
```

MongoDB remains available for inspection and SSH forwarding.

## Stop the complete platform

Stop in reverse dependency order:

```bash
cd /home/spider/projects/spider-doctor
docker compose stop

cd /home/spider/projects/spider-executor
docker compose stop
```

`docker compose stop` preserves containers, networks, and named volumes.

## Remove application containers without deleting data

Only for a deliberate clean container recreation:

```bash
cd /home/spider/projects/spider-doctor
docker compose down

cd /home/spider/projects/spider-executor
docker compose down
```

Do **not** add `--volumes`. MongoDB and Executor artifacts are in named volumes.

---

# 4. Restart operations

## Restart Doctor only

```bash
cd /home/spider/projects/spider-doctor
docker compose restart doctor
docker compose ps doctor
```

Inspect logs afterward:

```bash
docker compose logs --no-color --since=5m doctor
```

## Restart Executor worker only

```bash
cd /home/spider/projects/spider-executor
docker compose restart worker
docker compose ps worker
```

## Restart API only

```bash
cd /home/spider/projects/spider-executor
docker compose restart api
curl --fail-with-body http://127.0.0.1:8000/health/ready
```

## Restart runner only

Pause the worker first so it cannot submit a run during the restart:

```bash
cd /home/spider/projects/spider-executor
docker compose stop worker
docker compose restart runner
docker compose up -d --wait --wait-timeout 180 runner
docker compose start worker
docker compose ps runner worker
```

## Restart MongoDB safely

Stop Doctor and Executor processing first:

```bash
cd /home/spider/projects/spider-doctor
docker compose stop doctor

cd /home/spider/projects/spider-executor
docker compose stop worker api
docker compose restart mongo
docker compose up -d --wait --wait-timeout 180 mongo mongo-init
docker compose start api worker
curl --fail-with-body http://127.0.0.1:8000/health/ready
```

Then restart Doctor:

```bash
cd /home/spider/projects/spider-doctor
./scripts/start.sh
```

## Restart the complete platform

```bash
cd /home/spider/projects/spider-doctor
docker compose stop

cd /home/spider/projects/spider-executor
docker compose stop
docker compose up -d --wait --wait-timeout 180
curl --fail-with-body http://127.0.0.1:8000/health/ready

cd /home/spider/projects/spider-doctor
./scripts/start.sh
```

---

# 5. Update deployment from Git

## Pre-update checks

Confirm host, user, and repository state:

```bash
whoami
hostname
for repo in spider-scripts spider-executor spider-doctor spider-devops; do
  git -C "/home/spider/projects/$repo" status --short --branch
done
```

Do not proceed if a production checkout has unexpected modifications.

Check for active Doctor task containers:

```bash
docker ps \
  --filter 'label=spider-doctor.managed=true' \
  --format 'table {{.Names}}\t{{.Status}}'
```

Let a healthy task finish before routine maintenance.

## Update Executor

Stop Doctor first:

```bash
cd /home/spider/projects/spider-doctor
docker compose stop doctor
```

Update and rebuild Executor:

```bash
cd /home/spider/projects/spider-executor
git pull --ff-only
docker compose config --quiet
docker compose up --build -d --wait --wait-timeout 180
curl --fail-with-body http://127.0.0.1:8000/health/ready
docker compose ps -a
```

Restart Doctor after Executor is healthy:

```bash
cd /home/spider/projects/spider-doctor
./scripts/start.sh
```

## Update Doctor

Stop Doctor before updating its code:

```bash
cd /home/spider/projects/spider-doctor
docker compose stop doctor
git pull --ff-only
docker compose config --quiet
./scripts/start.sh
```

Do not rerun `scripts/configure-hermes.sh` during a normal code update.

## Update operations documentation

```bash
cd /home/spider/projects/spider-devops
git pull --ff-only
```

## Update `spider-scripts`

The Executor worker provisions exact Doctor commits automatically. For manual synchronization, first ensure the checkout is clean:

```bash
cd /home/spider/projects/spider-scripts
git status --short --branch
git pull --ff-only
```

Never reset or clean unfamiliar changes.

---

# 6. Logs

## Executor logs

All recent Executor logs:

```bash
cd /home/spider/projects/spider-executor
docker compose logs --no-color --since=10m mongo mongo-init api worker runner
```

Follow worker logs:

```bash
docker compose logs --no-color -f worker
```

Follow runner logs:

```bash
docker compose logs --no-color -f runner
```

## Doctor logs

```bash
cd /home/spider/projects/spider-doctor
docker compose logs --no-color --since=10m doctor broker egress-proxy
```

Follow Doctor dispatcher:

```bash
docker compose logs --no-color -f doctor
```

Follow restricted proxy traffic:

```bash
docker compose logs --no-color -f egress-proxy
```

Press `Ctrl+C` to stop following logs. This does not stop a service.

## Disposable task logs

List active task containers:

```bash
docker ps \
  --filter 'label=spider-doctor.managed=true' \
  --format 'table {{.Names}}\t{{.Status}}'
```

Find one task by its MongoDB task ID:

```bash
docker ps -a \
  --filter 'label=spider-doctor.task-id=TASK_ID' \
  --format 'table {{.Names}}\t{{.Status}}'
```

Follow it if still present:

```bash
container_id=$(docker ps -q --filter 'label=spider-doctor.task-id=TASK_ID')
if [ -n "$container_id" ]; then
  docker logs -f "$container_id"
else
  echo 'No active container; inspect the durable MongoDB task.'
fi
```

Replace `TASK_ID` exactly.

---

# 7. Register and monitor work

## Register an entry

```bash
curl --fail-with-body -sS \
  -X POST http://127.0.0.1:8000/api/v1/register \
  -H 'content-type: application/json' \
  --data-binary @- <<'JSON'
{
  "entry_id": "EXACT_ENTRY_ID",
  "businessname": "Exact business name",
  "address": "Exact address"
}
JSON
```

Registration returns `202 Accepted` after persisting the entry and create task. Doctor work is asynchronous.

## Correct a queued registration

Posting the same `entry_id` with a changed name or address updates the existing registration and resets its queued create task. Stop Doctor first so the task cannot be running:

```bash
cd /home/spider/projects/spider-doctor
docker compose stop doctor
```

Then post the corrected identity using the same `entry_id`. Identical data is idempotent and does not reset attempts. A correction while the create task is running fails closed.

Restart Doctor only after verifying the corrected entry and task.

## Inspect one Doctor task

```bash
docker exec spider-executor-mongo-1 mongosh --quiet spider --eval '
d=db.doctor_tasks.findOne({_id:"TASK_ID"});
if(!d){print("NOT_FOUND");quit(1)};
print("entry_id="+d.entry_id);
print("type="+d.type);
print("status="+d.status);
print("attempts="+d.attempts);
print("max_attempts="+d.max_attempts);
print("lease="+JSON.stringify(d.lease));
print("candidate_sha="+(d.candidate_sha||"NONE"));
print("commit_sha="+((d.result&&d.result.commit_sha)||"NONE"));
print("last_error="+(d.last_error||"NONE"));
'
```

## List recent Doctor tasks

```bash
docker exec spider-executor-mongo-1 mongosh --quiet spider --eval '
db.doctor_tasks.find(
  {},
  {_id:1,entry_id:1,type:1,status:1,attempts:1,max_attempts:1,candidate_sha:1,last_error:1,updated_at:1}
).sort({updated_at:-1}).limit(20).forEach(printjson)
'
```

Do not infer the exact error from the generic Doctor log summary. Use `last_error` in the durable task.

## Manually enqueue an activated scraper

```bash
curl --fail-with-body -sS \
  -X POST http://127.0.0.1:8000/api/v1/execution-jobs \
  -H 'content-type: application/json' \
  --data-binary @- <<'JSON'
{
  "entry_id": "EXACT_ENTRY_ID",
  "trigger": "manual",
  "idempotency_key": "manual:EXACT_ENTRY_ID:UNIQUE_VALUE"
}
JSON
```

Use a unique, meaningful idempotency key for a new run. Reusing a key returns/deduplicates the existing job.

---

# 8. MongoDB access and SSH forwarding

MongoDB is published only on VM loopback:

```text
127.0.0.1:27017
```

Verify on the VM:

```bash
ss -ltn | grep '127.0.0.1:27017'
docker exec spider-executor-mongo-1 mongosh --quiet spider --eval 'printjson(db.adminCommand("ping"))'
```

From a local computer, open an SSH tunnel:

```bash
ssh -N -L 27017:127.0.0.1:27017 spider@spider-01
```

Then connect the local MongoDB client to:

```text
mongodb://127.0.0.1:27017/spider?replicaSet=rs0&directConnection=true
```

Keep the SSH session open. Never change the Compose binding to `0.0.0.0` merely for remote access.

---

# 9. Health and preflight checks

## Executor readiness

```bash
curl --fail-with-body http://127.0.0.1:8000/health/ready
```

## MongoDB replica-set primary

```bash
docker exec spider-executor-mongo-1 mongosh --quiet --eval 'printjson(db.hello())'
```

Look for:

```text
isWritablePrimary: true
```

## Doctor fail-closed preflight

```bash
cd /home/spider/projects/spider-doctor
python3 scripts/preflight.py
```

Preflight must pass before Doctor processes untrusted task work.

## Task egress network

```bash
docker network inspect spider-doctor-egress \
  --format 'name={{.Name}} internal={{.Internal}} policy={{index .Labels "spider-doctor.egress-policy"}}'
```

Expected:

```text
internal=true
policy=restricted-v1
```

---

# 10. Common incidents

## Registration returns queued but nothing happens

1. Confirm Doctor is running.
2. Query the exact task by returned task ID.
3. If `queued`, check `available_at` and Doctor logs.
4. If `running`, find the disposable task container.
5. If `failed`, `exhausted`, or requeued, inspect `last_error`.
6. Do not submit a duplicate registration unless correcting the stored identity.

## Repeated `Doctor attempt status=failed`

Stop Doctor immediately:

```bash
cd /home/spider/projects/spider-doctor
docker compose stop doctor
```

Query the exact durable task. Do not consume another attempt until the failure is classified as identity, scraper-generation, publication, or infrastructure.

## Repeated `awaiting_review` for an already published candidate

Keep Doctor stopped and verify:

- task `candidate_sha`
- task `result.commit_sha`
- remote commit ancestry
- current Doctor version includes published-candidate reconciliation

Matching candidate and commit SHAs should reconcile to `succeeded` with `lease=null`; the task must not replay.

## Worker cannot write `/srv/spider/locks/scripts.lock`

Confirm `runtime-init` exited zero:

```bash
cd /home/spider/projects/spider-executor
docker compose ps -a runtime-init
docker compose logs --no-color runtime-init
```

Do not delete the runtime volume. Recreate the reviewed one-shot initializer:

```bash
docker compose up --force-recreate runtime-init
docker compose up -d worker runner
```

## Executor cannot fetch private `spider-scripts`

Check the trusted worker only:

```bash
docker exec spider-executor-worker-1 sh -lc '
  command -v ssh
  test -r /app/.ssh/id_ed25519
  git ls-remote git@github.com:cl0udarch1t3cts/spider-scripts.git HEAD
'
```

Do not mount SSH credentials into API, runner, MongoDB, or disposable Doctor task containers.

## Executor API is unavailable

```bash
cd /home/spider/projects/spider-executor
docker compose ps -a api mongo mongo-init
docker compose logs --no-color --tail=200 api mongo mongo-init
curl -v http://127.0.0.1:8000/health/ready
```

## Doctor broker is unhealthy

```bash
cd /home/spider/projects/spider-doctor
docker compose ps -a broker
docker compose logs --no-color --tail=200 broker
```

Do not copy OAuth out of `data/broker-hermes` and do not place OAuth into `data/hermes`.

## MongoDB fails after host/kernel changes

The production override pins both `mongo` and `mongo-init` to `7.0.40`. Verify the effective configuration:

```bash
cd /home/spider/projects/spider-executor
docker compose config --images
```

Do not bypass MongoDB compatibility guards or change only one of the two MongoDB services.

## A Compose command shows the wrong services

Compose is directory-specific. Confirm location:

```bash
pwd
```

Use plain `docker ps` for the whole host, or `cd` into the intended repository before `docker compose` commands.

---

# 11. Backup and recovery priorities

Authoritative data boundaries:

1. MongoDB contains registrations, Doctor tasks, execution jobs/runs, and production records.
2. GitHub `spider-scripts` contains published scraper source history.
3. `spider-doctor/data/broker-hermes` contains OAuth state and must be backed up securely outside Git.
4. Doctor task/workspace data can be required to resume a persisted candidate.

## MongoDB logical backup

Create a host backup directory and run `mongodump` inside the MongoDB container:

```bash
mkdir -p /home/spider/backups/mongodb
stamp=$(date -u +%Y%m%dT%H%M%SZ)
docker exec spider-executor-mongo-1 \
  mongodump --quiet --db spider --archive \
  > "/home/spider/backups/mongodb/spider-${stamp}.archive"
chmod 600 "/home/spider/backups/mongodb/spider-${stamp}.archive"
```

Verify the file exists and is non-empty:

```bash
test -s "/home/spider/backups/mongodb/spider-${stamp}.archive" && echo BACKUP_OK
```

A restore is destructive and must be planned separately. Do not run `mongorestore --drop` during routine operations.

---

# 12. Routine operator checklist

## Daily

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
curl --fail-with-body http://127.0.0.1:8000/health/ready
```

Review recent failures:

```bash
docker exec spider-executor-mongo-1 mongosh --quiet spider --eval '
db.doctor_tasks.find(
  {status:{$in:["queued","running","failed","exhausted","human_review_required"]}},
  {_id:1,entry_id:1,type:1,status:1,attempts:1,max_attempts:1,last_error:1,updated_at:1}
).sort({updated_at:-1}).limit(20).forEach(printjson)
'
```

## Before maintenance

- confirm host/user/path;
- confirm Git trees are clean;
- check active disposable task containers;
- stop Doctor;
- make a MongoDB backup for risky database changes.

## After maintenance

- Executor readiness passes;
- MongoDB is primary;
- runner and broker are healthy;
- Doctor preflight passes;
- Doctor dispatcher is up;
- localhost ports remain loopback-only;
- no unexpected task replay or retry loop appears in logs.
