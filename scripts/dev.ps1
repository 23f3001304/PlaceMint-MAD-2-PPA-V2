# Brings up the full PlaceMint dev stack, each service in its own window.
#
# Prerequisites (one-time):
#   - backend venv created + `pip install -r requirements.txt`
#   - frontend `npm install`
#   - Docker Desktop running (for Redis)
#
# Usage:  powershell -ExecutionPolicy Bypass -File scripts\dev.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$backend = Join-Path $root 'backend'
$frontend = Join-Path $root 'frontend'
$py = Join-Path $backend 'venv\Scripts\python.exe'
$celery = Join-Path $backend 'venv\Scripts\celery.exe'

function Start-Svc($title, $cmd) {
  Start-Process powershell -ArgumentList '-NoExit', '-Command', "`$Host.UI.RawUI.WindowTitle = '$title'; $cmd"
}

Write-Host 'Starting Redis (Docker container ppa-redis)...'
docker start ppa-redis 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { docker run -d --name ppa-redis -p 6379:6379 redis:alpine | Out-Null }
Start-Sleep -Seconds 2

Start-Svc 'PlaceMint API'  "Set-Location '$backend'; & '$py' run.py"
Start-Svc 'Celery worker'  "Set-Location '$backend'; `$env:PYTHONPATH = '.'; & '$celery' -A celery_worker.celery worker --pool=solo --loglevel=info"
Start-Svc 'Celery beat'    "Set-Location '$backend'; `$env:PYTHONPATH = '.'; & '$celery' -A celery_worker.celery beat --loglevel=info"
Start-Svc 'PlaceMint web'  "Set-Location '$frontend'; npm run dev"

Write-Host ''
Write-Host 'PlaceMint stack starting in separate windows:'
Write-Host '  Redis         localhost:6379   (Docker: ppa-redis)'
Write-Host '  Flask API     http://127.0.0.1:5000'
Write-Host '  Vue SPA       http://127.0.0.1:5173'
Write-Host '  Celery worker + beat'
Write-Host ''
Write-Host 'Stop everything: close the windows, then  docker stop ppa-redis'
