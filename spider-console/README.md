# spider-console

Read-only Next.js dashboard for the spider platform: live Doctor tasks,
execution runs, entries, and the subscription budget.

All data comes from HTTP APIs — the console never touches MongoDB directly:

- the Executor API (`/api/v1/stats`, `/api/v1/doctor-tasks`, `/api/v1/runs`,
  `/api/v1/entries`) over the `spider-executor_control` network, and
- the broker `/usage` endpoint over the `spider-doctor_uplink` network,
  authenticated with the Doctor proxy token.

## Deploy (on the VM, after Executor and Doctor are up)

```bash
cd /home/spider/projects/spider-runtime/spider-console
SPIDER_DOCTOR_HOST_ROOT=/home/spider/projects/spider-runtime/spider-doctor \
  docker compose up --build -d
```

Or from the repo root: `make console`.

## Access

The console binds to `127.0.0.1:8646` on the VM only (it has no auth).
From your machine:

```bash
ssh -N -L 8646:127.0.0.1:8646 spider-01
# then open http://localhost:8646
```

## Local development

```bash
npm install
EXECUTOR_API_URL=http://127.0.0.1:8000 npm run dev
```
