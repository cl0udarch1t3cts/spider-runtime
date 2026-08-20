#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

TASK_ID=${1:-}
if [[ ! $TASK_ID =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]]; then
  printf 'Usage: %s <task_id>\n' "$0" >&2
  exit 2
fi

TASK_DIR="data/tasks/$TASK_ID"
TASK_HOME="$TASK_DIR/hermes-home"

printf '%s\n' '=== Config versions ==='
for config in data/hermes/config.yaml "$TASK_HOME/config.yaml"; do
  if [[ -f $config ]]; then
    version=$(grep -E '^_config_version:' "$config" || true)
    printf '%s: %s\n' "$config" "${version:-MISSING}"
  else
    printf '%s: FILE MISSING\n' "$config"
  fi
done

printf '%s\n' '=== Ownership and modes ==='
for path in data/hermes data/hermes/config.yaml "$TASK_DIR" "$TASK_HOME" "$TASK_HOME/config.yaml"; do
  if [[ -e $path ]]; then
    stat -c '%u:%g mode=%a %n' "$path"
  else
    printf 'MISSING %s\n' "$path"
  fi
done

printf '%s\n' '=== Doctor container identity ==='
docker compose exec -T doctor id
