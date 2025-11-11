#!/usr/bin/env bash
set -euo pipefail
echo "== format =="
docker compose exec -T backend ruff check --fix || true
