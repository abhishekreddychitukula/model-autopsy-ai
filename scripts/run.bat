#model-autopsy-ai/run.bat this file starts the FastAPI backend server for windows systems

@echo off
REM Model Autopsy AI - Windows Run Script

REM Navigate to project root
cd /d "%~dp0.."

echo 🔬 Model Autopsy AI - Starting...

REM Check Python
python --version
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Create virtual environment if needed
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo ⚠️  Warning: .env file not found. Creating from .env.example...
    copy .env.example .env
    echo Please edit .env and add your API keys
)

REM Run the application
echo.
echo 🚀 Starting FastAPI server...
echo 📖 API Documentation: http://127.0.0.1:8000/docs
echo 🏥 Health Check: http://127.0.0.1:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
