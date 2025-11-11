Write-Host "== lint =="
docker compose exec -T backend ruff check
Push-Location frontend
npx eslint .
Pop-Location
