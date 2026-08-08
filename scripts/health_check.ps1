Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "          ZAI HEALTH CHECK" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

try {

    $response = Invoke-RestMethod `
        -Uri "http://127.0.0.1:8000/health" `
        -Method GET `
        -TimeoutSec 10

    Write-Host "BACKEND : ONLINE" -ForegroundColor Green
    Write-Host "STATUS  : $($response.status)" -ForegroundColor Green
    Write-Host "ASSISTANT : $($response.assistant)" -ForegroundColor Green

}
catch {

    Write-Host "BACKEND : OFFLINE" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red

}

Write-Host ""

try {

    $ollama = Invoke-RestMethod `
        -Uri "http://127.0.0.1:11434/api/tags" `
        -Method GET `
        -TimeoutSec 10

    Write-Host "OLLAMA  : ONLINE" -ForegroundColor Green

}
catch {

    Write-Host "OLLAMA  : OFFLINE" -ForegroundColor Red

}

Write-Host ""
