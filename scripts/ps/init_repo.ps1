Write-Host "== init_repo =="
if (-Not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
Push-Location backend
if (-Not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
Pop-Location
Push-Location frontend
if (-Not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
Pop-Location
Write-Host "OK"
