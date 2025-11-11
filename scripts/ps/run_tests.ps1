Write-Host "== tests =="
docker compose exec -T backend pytest -q
Push-Location frontend
npm test --silent
Pop-Location
