Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "           STARTING ZAI" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\ZAI\backend"

Write-Host "Starting FastAPI..." -ForegroundColor Yellow

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
