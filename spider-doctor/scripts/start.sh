#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
# Create the internal task network without starting any OAuth-bearing image.
docker compose up --build -d egress-proxy
python3 scripts/preflight.py
docker compose up --build -d --wait --wait-timeout 180
docker compose ps -a
