#!/usr/bin/env bash
set -euo pipefail

echo "== dev up =="

COMPOSE_FILE="infra/compose/docker-compose.dev.yml"
if [ ! -f "$COMPOSE_FILE" ]; then
  echo "[error] $COMPOSE_FILE is missing. Ensure Phase 1 scaffolding is applied." >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "[error] docker is not installed or not on PATH." >&2
  exit 1
fi

DOCKER_HOST_STATUS=$(docker info >/dev/null 2>&1 && echo ok || echo fail)
if [ "$DOCKER_HOST_STATUS" != "ok" ]; then
  echo "[error] unable to communicate with the Docker daemon." >&2
  exit 1
fi

DOCKER_COMPOSE=${DOCKER_COMPOSE:-"docker compose"}
$DOCKER_COMPOSE -f "$COMPOSE_FILE" up -d --build

echo "[ok] development stack is starting"
