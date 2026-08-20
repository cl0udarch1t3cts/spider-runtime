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

SOURCE_HOME="$PWD/data/tasks/$TASK_ID/hermes-home"
if [[ ! -f $SOURCE_HOME/config.yaml ]]; then
  printf 'Task config does not exist: %s/config.yaml\n' "$SOURCE_HOME" >&2
  exit 1
fi

PROBE_HOME="$PWD/data/tasks/$TASK_ID/entrypoint-probe-home"
rm -rf "$PROBE_HOME"
mkdir -m 0700 "$PROBE_HOME"
cp -p "$SOURCE_HOME/config.yaml" "$PROBE_HOME/config.yaml"
cleanup() {
  rm -rf "$PROBE_HOME"
}
trap cleanup EXIT

docker run --rm \
  --init \
  --network=none \
  --cap-drop=ALL \
  --cap-add=CHOWN \
  --cap-add=SETUID \
  --cap-add=SETGID \
  --security-opt=no-new-privileges:true \
  --pids-limit=256 \
  --memory=4g \
  --cpus=2 \
  --ulimit=nofile=1024:1024 \
  --env="HERMES_UID=${SPIDER_DOCTOR_UID}" \
  --env="HERMES_GID=${SPIDER_DOCTOR_GID}" \
  --tmpfs=/run:rw,noexec,nosuid,nodev,size=64m \
  --tmpfs=/tmp:rw,noexec,nosuid,nodev,size=256m \
  --volume="$PROBE_HOME:/opt/data:rw" \
  "nousresearch/hermes-agent@${SPIDER_DOCTOR_HERMES_DIGEST}" \
  sh -c 'id; stat -c "%u:%g mode=%a %n" /opt/data /opt/data/config.yaml; cd /opt/data; pwd'
