#!/usr/bin/env bash
set -euo pipefail

require_dir() {
  local path=$1
  if [ ! -d "$path" ]; then
    echo "[error] expected directory '$path' is missing. Run Phase 1 scaffolding or check the repository layout." >&2
    exit 1
  fi
}

copy_env() {
  local dir=$1
  if [ -f "$dir/.env.example" ] && [ ! -f "$dir/.env" ]; then
    cp "$dir/.env.example" "$dir/.env"
    echo "[info] copied $dir/.env from template"
  fi
}

echo "== init_repo =="

require_dir backend
require_dir frontend

if [ -f ".env.example" ] && [ ! -f ".env" ]; then
  cp ".env.example" ".env"
  echo "[info] copied project .env from template"
fi

copy_env backend
copy_env frontend

echo "[ok] repository initialization complete"
