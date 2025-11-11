Write-Host "== format =="
docker compose exec -T backend ruff check --fix || exit 0
