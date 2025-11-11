#!/usr/bin/env bash
set -euo pipefail
echo "== dev up =="
docker compose up -d --build
