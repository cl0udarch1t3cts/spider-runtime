#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -f .env ]]; then
  printf 'Missing .env. Copy .env.example to .env and set the required values.\n' >&2
  exit 1
fi

set -a
# .env is operator-owned settings only; credentials stay in data/.
. ./.env
set +a

if [[ ! ${SPIDER_DOCTOR_HERMES_DIGEST:-} =~ ^sha256:[0-9a-f]{64}$ ]]; then
  printf 'SPIDER_DOCTOR_HERMES_DIGEST must be a full reviewed sha256 digest.\n' >&2
  exit 1
fi
HERMES_IMAGE="nousresearch/hermes-agent@${SPIDER_DOCTOR_HERMES_DIGEST}"
if [[ ${SPIDER_DOCTOR_HOST_ROOT:-} != "$PWD" ]]; then
  printf 'SPIDER_DOCTOR_HOST_ROOT must equal this absolute checkout path: %s\n' "$PWD" >&2
  exit 1
fi

mkdir -p data/broker-hermes data/hermes data/tasks data/workspaces
if [[ ! -f data/proxy-token ]]; then
  umask 077
  openssl rand -hex 32 > data/proxy-token
fi
chmod 0600 data/proxy-token

# This credential-free home is deployment-generated, not user-authored. Re-seed
# its config from the pinned stock image so an old schema cannot block boot.
rm -f data/hermes/config.yaml data/hermes/config.yaml.bak-*

common=(
  --rm
  -e "HERMES_UID=${SPIDER_DOCTOR_UID}"
  -e "HERMES_GID=${SPIDER_DOCTOR_GID}"
)

run_task_hermes() {
  docker run "${common[@]}" \
    -v "${SPIDER_DOCTOR_HOST_ROOT}/data/hermes:/opt/data:rw" \
    "$HERMES_IMAGE" "$@"
}

run_task_hermes config set providers.doctor-codex.api http://spider-doctor-broker:8645/v1
run_task_hermes config set providers.doctor-codex.transport codex_responses
# Second broker-fronted provider for policy-routed models (ADR-008): same
# broker endpoint and client token, plain OpenAI chat/completions transport.
run_task_hermes config set providers.doctor-openrouter.api http://spider-doctor-broker:8645/v1
run_task_hermes config set providers.doctor-openrouter.transport chat_completions
run_task_hermes config set providers.doctor-openrouter.key_cmd 'cat /task/proxy-token'
run_task_hermes config set providers.doctor-codex.key_cmd 'cat /task/proxy-token'
run_task_hermes config set providers.doctor-codex.default_model "${SPIDER_DOCTOR_MODEL:-gpt-5.4}"
run_task_hermes config set model.provider custom:doctor-codex
run_task_hermes config set model.default "${SPIDER_DOCTOR_MODEL:-gpt-5.4}"
run_task_hermes config check

# Stock Hermes seeds a non-secret .env template at container bootstrap. It is
# unnecessary for task execution and the dispatcher intentionally refuses any
# persisted .env in the credential-free seed home.
rm -f data/hermes/.env
if [[ -s data/hermes/auth.json ]]; then
  printf 'Credential material must not exist in the disposable task Hermes home.\n' >&2
  exit 1
fi

if [[ ! -s data/broker-hermes/auth.json ]]; then
  printf '\nAuthenticate the trusted broker with OpenAI Codex OAuth.\n'
  docker run -it "${common[@]}" \
    -v "${SPIDER_DOCTOR_HOST_ROOT}/data/broker-hermes:/opt/data:rw" \
    "$HERMES_IMAGE" auth add openai-codex
fi

printf '\nHermes homes configured. OAuth exists only in data/broker-hermes.\n'
printf 'Do not start Compose until the restricted task-egress network has been enforced and attested.\n'
