#!/usr/bin/env bash
set -euo pipefail
echo "== smoke =="
set +e
curl -sf http://localhost:8000/api/v1/health || echo "backend not ready"
set -e
