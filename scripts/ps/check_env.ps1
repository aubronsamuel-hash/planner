Write-Host "== check env =="
if (-Not (Test-Path ".env")) { Write-Host "Missing .env at root"; exit 1 }
if (-Not (Test-Path "backend/.env")) { Write-Host "Missing backend/.env"; exit 1 }
if (-Not (Test-Path "frontend/.env")) { Write-Host "Missing frontend/.env"; exit 1 }
Write-Host "env OK"
