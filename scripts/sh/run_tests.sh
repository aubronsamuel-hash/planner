#!/usr/bin/env bash
set -euo pipefail
echo "== tests =="
docker compose exec -T backend pytest -q
( cd frontend && npm test --silent )
