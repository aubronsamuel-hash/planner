Write-Host "== migrate =="
docker compose exec -T backend alembic upgrade head
