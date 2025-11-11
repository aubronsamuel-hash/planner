#!/usr/bin/env bash
set -euo pipefail

echo "== dev down =="

COMPOSE_FILE="infra/compose/docker-compose.dev.yml"
if [ ! -f "$COMPOSE_FILE" ]; then
  echo "[warn] $COMPOSE_FILE missing; nothing to stop." >&2
  exit 0
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "[error] docker is not installed or not on PATH." >&2
  exit 1
fi

DOCKER_COMPOSE=${DOCKER_COMPOSE:-"docker compose"}
$DOCKER_COMPOSE -f "$COMPOSE_FILE" down -v

echo "[ok] development stack stopped"
