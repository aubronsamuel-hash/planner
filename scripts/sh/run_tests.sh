#!/usr/bin/env bash
set -euo pipefail

echo "== tests =="

if [ ! -d backend ]; then
  echo "[error] backend directory missing; run Phase 1 scaffolding." >&2
  exit 1
fi

if [ ! -d frontend ]; then
  echo "[error] frontend directory missing; run Phase 1 scaffolding." >&2
  exit 1
fi

if [ -f "backend/pyproject.toml" ]; then
  python -m pytest backend/tests
else
  echo "[warn] backend/pyproject.toml not found; skipping backend tests." >&2
fi

if [ -f "frontend/package.json" ]; then
  if command -v npm >/dev/null 2>&1; then
    echo "[info] install frontend dependencies"
    ( cd frontend && npm install >/dev/null 2>&1 && npm test --silent )
  else
    echo "[warn] npm is unavailable; skipping frontend tests." >&2
  fi
else
  echo "[warn] frontend/package.json not found; skipping frontend tests." >&2
fi

echo "[ok] test workflow completed"
