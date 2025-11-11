#!/usr/bin/env bash
set -euo pipefail
echo "== check env =="
[ -f ".env" ] || { echo "Missing .env at root"; exit 1; }
[ -f "backend/.env" ] || { echo "Missing backend/.env"; exit 1; }
[ -f "frontend/.env" ] || { echo "Missing frontend/.env"; exit 1; }
echo "env OK"
