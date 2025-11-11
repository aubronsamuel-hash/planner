#!/usr/bin/env bash
set -euo pipefail
echo "== lint =="
docker compose exec -T backend ruff check
( cd frontend && npx eslint . )
