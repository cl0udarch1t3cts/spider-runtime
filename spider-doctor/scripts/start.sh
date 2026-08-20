#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
# Create the internal task network and its only two dual-homed gateways first.
docker compose up --build -d egress-proxy broker
python3 scripts/preflight.py
docker compose up --build -d --wait --wait-timeout 180
docker compose ps -a
