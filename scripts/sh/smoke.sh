#!/usr/bin/env bash
set -euo pipefail

echo "== smoke =="

BACKEND_URL=${BACKEND_URL:-"http://localhost:8000/api/v1/health"}
if ! command -v curl >/dev/null 2>&1; then
  echo "[error] curl not installed; cannot run smoke test." >&2
  exit 1
fi

if ! curl -sf "$BACKEND_URL" >/dev/null 2>&1; then
  echo "[warn] backend not ready at $BACKEND_URL" >&2
  exit 1
fi

echo "[ok] backend health endpoint reachable"
