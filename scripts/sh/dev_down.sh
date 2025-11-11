#!/usr/bin/env bash
set -euo pipefail
echo "== dev down =="
docker compose down -v
