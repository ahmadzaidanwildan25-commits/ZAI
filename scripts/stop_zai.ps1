Write-Host ""
Write-Host "Stopping ZAI..." -ForegroundColor Yellow

Get-Process python -ErrorAction SilentlyContinue |
    Stop-Process -Force

Write-Host "ZAI stopped." -ForegroundColor Green
