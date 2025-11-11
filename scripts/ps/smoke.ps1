Write-Host "== smoke =="
try {
  $r = Invoke-WebRequest -Uri http://localhost:8000/api/v1/health -UseBasicParsing
  Write-Host $r.Content
} catch { Write-Host "backend not ready" }
