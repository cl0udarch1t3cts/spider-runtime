#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

TASK_ID=${1:-}
if [[ ! $TASK_ID =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]]; then
  printf 'Usage: %s <task_id>\n' "$0" >&2
  exit 2
fi

total_bytes=0
total_entries=0
printf '%-52s %14s %10s\n' PATH BYTES ENTRIES
for path in \
  "data/workspaces/$TASK_ID" \
  "data/tasks/$TASK_ID/output" \
  "data/tasks/$TASK_ID/hermes-home"; do
  if [[ ! -e $path ]]; then
    printf '%-52s %14s %10s\n' "$path" MISSING MISSING
    continue
  fi
  bytes=$(du -sb -- "$path" | cut -f1)
  entries=$(find "$path" -mindepth 1 -printf '.\n' | wc -l)
  total_bytes=$((total_bytes + bytes))
  total_entries=$((total_entries + entries))
  printf '%-52s %14d %10d\n' "$path" "$bytes" "$entries"
done
printf '%-52s %14d %10d\n' TOTAL "$total_bytes" "$total_entries"
printf '%-52s %14d %10d\n' LIMIT "$((512 * 1024 * 1024))" 20000

printf '\nLargest task-home children:\n'
du -sb -- "data/tasks/$TASK_ID/hermes-home"/* 2>/dev/null | sort -nr | head -20 || true
