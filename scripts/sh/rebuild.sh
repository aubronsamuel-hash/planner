#!/usr/bin/env bash
set -euo pipefail
echo "== rebuild =="
docker compose down -v
docker compose up -d --build
