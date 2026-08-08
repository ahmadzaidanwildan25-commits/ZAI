@echo off
title ZAI AI

echo ==========================================
echo                 ZAI AI
echo          Starting ZAI System...
echo ==========================================
echo.

echo [1/2] Starting ZAI Backend...

start "ZAI Backend" cmd /k "cd /d C:\ZAI\backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo.
echo Menunggu backend...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] Starting ZAI Frontend...

start "" "C:\ZAI\frontend\build\windows\x64\runner\Release\frontend.exe"

echo.
echo ==========================================
echo              ZAI IS ONLINE
echo ==========================================
echo.

exit