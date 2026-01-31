# Model Autopsy AI - Windows Start Script used to start both backend and frontend servers for windows systems

@echo off
echo ========================================
echo   Model Autopsy AI - Quick Start
echo ========================================
echo.

echo Starting Backend Server (FastAPI)...
echo Backend will run on: http://127.0.0.1:8000
echo.

start cmd /k "cd /d "%~dp0.." && echo Starting FastAPI Backend... && uvicorn app.main:app --reload"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server (React + Vite)...
echo Frontend will run on: http://localhost:3000
echo.

start cmd /k "cd /d "%~dp0..\frontend" && echo Starting React Frontend... && npm run dev"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   SERVERS STARTING!
echo ========================================
echo.
echo Backend API:  http://127.0.0.1:8000
echo API Docs:     http://127.0.0.1:8000/docs
echo Frontend:     http://localhost:3000
echo.
echo Press any key to open frontend in browser...
pause >nul

start http://localhost:3000

echo.
echo To stop servers: Close the terminal windows
echo ========================================
