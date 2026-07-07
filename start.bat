@echo off
title Domain Intelligence Agent

echo =====================================================
echo   Domain Intelligence Agent - Startup
echo =====================================================
echo.

REM --- Start Puppeteer Screenshot Service ---
echo [1/2] Starting Puppeteer screenshot service on port 3000...
start "Screenshot Service (port 3000)" cmd /k "cd /d "%~dp0screenshot-service" && node server.js"

REM Give Node a moment to initialize
timeout /t 2 /nobreak >nul

REM --- Start Streamlit App ---
echo [2/2] Starting Streamlit app...
echo.
cd /d "%~dp0agent"
py -m streamlit run app.py

pause
