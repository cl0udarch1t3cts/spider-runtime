#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

TASK_ID=${1:-}
if [[ ! $TASK_ID =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]]; then
  printf 'Usage: %s <task_id>\n' "$0" >&2
  exit 2
fi
if [[ ! -f .env ]]; then
  printf 'Missing .env.\n' >&2
  exit 1
fi

set -a
# shellcheck disable=SC1091
. ./.env
set +a

if [[ ! ${SPIDER_DOCTOR_HERMES_DIGEST:-} =~ ^sha256:[0-9a-f]{64}$ ]]; then
  printf 'SPIDER_DOCTOR_HERMES_DIGEST must be a full sha256 digest.\n' >&2
  exit 1
fi

TASK_HOME="$PWD/data/tasks/$TASK_ID/hermes-home"
if [[ ! -d $TASK_HOME ]]; then
  printf 'Task home does not exist: %s\n' "$TASK_HOME" >&2
  exit 1
fi

docker run --rm \
  --network=none \
  --entrypoint /bin/sh \
  --user "${SPIDER_DOCTOR_UID}:${SPIDER_DOCTOR_GID}" \
  --volume="$TASK_HOME:/opt/data:rw" \
  "nousresearch/hermes-agent@${SPIDER_DOCTOR_HERMES_DIGEST}" \
  -c 'id; stat -c "%u:%g mode=%a %n" /opt/data /opt/data/config.yaml; cd /opt/data; pwd'
