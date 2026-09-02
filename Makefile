# Convenience wrapper over the two Compose stacks. The stacks stay separate
# projects on purpose (see docs/OPERATIONS.md, which remains the
# authoritative runbook); every target here mirrors a documented procedure,
# including its ordering constraints.

EXECUTOR_DIR := $(CURDIR)/spider-executor
DOCTOR_DIR   := $(CURDIR)/spider-doctor
CONSOLE_DIR  := $(CURDIR)/spider-console
HEALTH_URL   := http://127.0.0.1:8000/health/ready
WAIT         := --wait --wait-timeout 180

.DEFAULT_GOAL := help

.PHONY: help status health usage reauth conversation console console-down console-logs \
	up start-doctor stop stop-doctor stop-doctor-stack \
	stop-executor-apps down restart-doctor restart-worker restart-api \
	restart-runner restart-mongo restart-all pull update update-doctor \
	logs logs-executor logs-doctor tail tail-doctor tail-worker tail-runner tail-proxy

help: ## List available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[1m%-20s\033[0m %s\n", $$1, $$2}'

status: ## Show container status of both stacks
	@docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
	@echo "--- executor ---"
	@cd $(EXECUTOR_DIR) && docker compose ps -a
	@echo "--- doctor ---"
	@cd $(DOCTOR_DIR) && docker compose ps -a

health: ## Check the Executor readiness endpoint
	curl --fail-with-body $(HEALTH_URL)

# The console shares the Doctor's .env so budget knobs stay in sync.
console: ## Build and start the read-only console on 127.0.0.1:8646 (access via SSH tunnel)
	cd $(CONSOLE_DIR) && docker compose --env-file $(DOCTOR_DIR)/.env up --build -d
	@echo "console up; open a tunnel: ssh -N -L 8646:127.0.0.1:8646 <vm> then http://localhost:8646"

console-down: ## Stop the console
	cd $(CONSOLE_DIR) && docker compose --env-file $(DOCTOR_DIR)/.env down

console-logs: ## Recent console logs
	cd $(CONSOLE_DIR) && docker compose --env-file $(DOCTOR_DIR)/.env logs --no-color --since=10m

conversation: ## Show a Doctor task's Hermes transcript: make conversation TASK=<id> (omit TASK to list recent)
	@python3 $(DOCTOR_DIR)/scripts/doctor-conversation.py $(TASK)

usage: ## Show current subscription usage via the broker (budget gate source)
	@cd $(DOCTOR_DIR) && docker compose exec doctor python3 -c 'import os, json, urllib.request; \
		token = open(os.environ["SPIDER_DOCTOR_PROXY_TOKEN_FILE"]).read().strip(); \
		req = urllib.request.Request("http://broker:8645/usage", headers={"Authorization": "Bearer " + token}); \
		print(json.dumps(json.load(urllib.request.urlopen(req, timeout=60)), indent=2))'

# Interactive: configure-hermes.sh launches the Codex OAuth login in a TTY, and
# it only does so when auth.json is absent — hence the timestamped archive first
# (matching the existing auth.json.expired convention; OAuth stays in
# data/broker-hermes, which is never committed).
reauth: ## Re-authenticate the broker's Codex OAuth after expiry or a plan change (interactive)
	cd $(DOCTOR_DIR) && docker compose stop doctor
	cd $(DOCTOR_DIR) && if [ -s data/broker-hermes/auth.json ]; then \
		mv data/broker-hermes/auth.json data/broker-hermes/auth.json.expired-$$(date +%Y%m%d-%H%M%S); \
	fi
	cd $(DOCTOR_DIR) && ./scripts/configure-hermes.sh
	cd $(DOCTOR_DIR) && docker compose up -d $(WAIT) broker
	curl --fail-with-body $(HEALTH_URL)
	cd $(DOCTOR_DIR) && docker compose start doctor && docker compose ps doctor
	$(MAKE) usage
	@echo "Reauth complete. If the Doctor was paused via the console, unpause it there."

# --- start -------------------------------------------------------------------

up: ## Full platform start: Executor first, verify health, then Doctor
	cd $(EXECUTOR_DIR) && docker compose up -d $(WAIT)
	curl --fail-with-body $(HEALTH_URL)
	cd $(DOCTOR_DIR) && ./scripts/start.sh

start-doctor: ## Start only the Doctor service (Executor must already be healthy)
	curl --fail-with-body $(HEALTH_URL)
	cd $(DOCTOR_DIR) && docker compose start doctor && docker compose ps doctor

# --- stop --------------------------------------------------------------------

stop: ## Stop the complete platform in reverse dependency order (keeps containers and data)
	cd $(DOCTOR_DIR) && docker compose stop
	cd $(EXECUTOR_DIR) && docker compose stop

stop-doctor: ## Stop Doctor processing only; broker and proxy stay up
	cd $(DOCTOR_DIR) && docker compose stop doctor && docker compose ps doctor

stop-doctor-stack: ## Stop Doctor, broker, and egress proxy
	cd $(DOCTOR_DIR) && docker compose stop

stop-executor-apps: ## Stop worker/api/runner but leave MongoDB running (stops Doctor first)
	cd $(DOCTOR_DIR) && docker compose stop doctor
	cd $(EXECUTOR_DIR) && docker compose stop worker api runner

down: ## Remove application containers WITHOUT deleting data (never pass --volumes)
	cd $(DOCTOR_DIR) && docker compose down
	cd $(EXECUTOR_DIR) && docker compose down

# --- restart -----------------------------------------------------------------

restart-doctor: ## Restart the Doctor service and show recent logs
	cd $(DOCTOR_DIR) && docker compose restart doctor && docker compose ps doctor \
		&& docker compose logs --no-color --since=5m doctor

restart-worker: ## Restart the Executor worker
	cd $(EXECUTOR_DIR) && docker compose restart worker && docker compose ps worker

restart-api: ## Restart the Executor API and verify health
	cd $(EXECUTOR_DIR) && docker compose restart api
	curl --fail-with-body $(HEALTH_URL)

restart-runner: ## Restart the runner; pauses the worker so no run is submitted mid-restart
	cd $(EXECUTOR_DIR) && docker compose stop worker \
		&& docker compose restart runner \
		&& docker compose up -d $(WAIT) runner \
		&& docker compose start worker \
		&& docker compose ps runner worker

restart-mongo: ## Restart MongoDB safely: stop Doctor and Executor processing first
	cd $(DOCTOR_DIR) && docker compose stop doctor
	cd $(EXECUTOR_DIR) && docker compose stop worker api \
		&& docker compose restart mongo \
		&& docker compose up -d $(WAIT) mongo mongo-init \
		&& docker compose start api worker
	curl --fail-with-body $(HEALTH_URL)
	cd $(DOCTOR_DIR) && ./scripts/start.sh

restart-all: ## Restart the complete platform
	cd $(DOCTOR_DIR) && docker compose stop
	cd $(EXECUTOR_DIR) && docker compose stop \
		&& docker compose up -d $(WAIT)
	curl --fail-with-body $(HEALTH_URL)
	cd $(DOCTOR_DIR) && ./scripts/start.sh

# --- update ------------------------------------------------------------------

pull: ## Pull the monorepo only; no rebuild, no restarts
	git -C $(CURDIR) pull --ff-only

update: ## Pull the monorepo and redeploy: stop Doctor, rebuild Executor, restart Doctor
	@docker ps --filter 'label=spider-doctor.managed=true' --format 'table {{.Names}}\t{{.Status}}'
	cd $(DOCTOR_DIR) && docker compose stop doctor
	git -C $(CURDIR) pull --ff-only
	cd $(EXECUTOR_DIR) && docker compose config --quiet \
		&& docker compose up --build -d $(WAIT)
	curl --fail-with-body $(HEALTH_URL)
	cd $(EXECUTOR_DIR) && docker compose ps -a
	cd $(DOCTOR_DIR) && ./scripts/start.sh

update-doctor: ## Pull the monorepo and redeploy only the Doctor
	cd $(DOCTOR_DIR) && docker compose stop doctor
	git -C $(CURDIR) pull --ff-only
	cd $(DOCTOR_DIR) && docker compose config --quiet && ./scripts/start.sh

# --- logs --------------------------------------------------------------------

logs: logs-executor logs-doctor ## Recent logs from both stacks

logs-executor: ## Last 10 minutes of Executor logs
	cd $(EXECUTOR_DIR) && docker compose logs --no-color --since=10m mongo mongo-init api worker runner

logs-doctor: ## Last 10 minutes of Doctor stack logs
	cd $(DOCTOR_DIR) && docker compose logs --no-color --since=10m doctor broker egress-proxy

tail: ## Follow all services of both stacks (Ctrl+C stops following, not the services)
	@(cd $(EXECUTOR_DIR) && docker compose logs --no-color -f) & \
	(cd $(DOCTOR_DIR) && docker compose logs --no-color -f) & \
	wait

tail-doctor: ## Follow the Doctor dispatcher (Ctrl+C stops following, not the service)
	cd $(DOCTOR_DIR) && docker compose logs --no-color -f doctor

tail-worker: ## Follow the Executor worker
	cd $(EXECUTOR_DIR) && docker compose logs --no-color -f worker

tail-runner: ## Follow the Executor runner
	cd $(EXECUTOR_DIR) && docker compose logs --no-color -f runner

tail-proxy: ## Follow restricted egress-proxy traffic
	cd $(DOCTOR_DIR) && docker compose logs --no-color -f egress-proxy
