#!/usr/bin/env bash
set -euo pipefail
echo "== migrate =="
docker compose exec -T backend alembic upgrade head
