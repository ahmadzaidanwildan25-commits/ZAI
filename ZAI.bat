@echo off
title ZAI AI

echo ========================================
echo              ZAI AI
echo       Personal AI Assistant
echo ========================================
echo.

echo [1/3] Memeriksa Ollama...
ollama list >nul 2>&1

if errorlevel 1 (
    echo Ollama belum berjalan.
    echo Menjalankan Ollama...
    start "" "ollama"
    timeout /t 3 /nobreak >nul
)

echo [2/3] Menjalankan ZAI Backend...

start "ZAI Backend" cmd /k "cd /d C:\ZAI\backend && python -m uvicorn app.main:app"

timeout /t 3 /nobreak >nul

echo [3/3] Menjalankan ZAI...

start "" "C:\ZAI\frontend\build\windows\x64\runner\Release\frontend.exe"

echo.
echo ZAI berhasil dijalankan.
echo.