#!/usr/bin/env bash
set -euo pipefail
echo "== init_repo =="
[ -f ".env" ] || cp ".env.example" ".env"
pushd backend >/dev/null
[ -f ".env" ] || cp ".env.example" ".env"
popd >/dev/null
pushd frontend >/dev/null
[ -f ".env" ] || cp ".env.example" ".env"
popd >/dev/null
echo "OK"
