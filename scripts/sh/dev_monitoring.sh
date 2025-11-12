#!/usr/bin/env bash
set -euo pipefail

echo "== dev monitoring up =="

COMPOSE_FILE="infra/compose/docker-compose.dev.yml"
if [ ! -f "$COMPOSE_FILE" ]; then
  echo "[error] $COMPOSE_FILE missing" >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "[error] docker is not installed or not on PATH." >&2
  exit 1
fi

DOCKER_COMPOSE=${DOCKER_COMPOSE:-"docker compose"}
$DOCKER_COMPOSE -f "$COMPOSE_FILE" up -d backend worker redis prometheus grafana loki

echo "[ok] monitoring stack is starting"
