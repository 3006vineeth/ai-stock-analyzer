@echo off
REM AI Stock Analyzer - Backend Startup Script for Windows

echo ==========================================
echo   AI Stock Analyzer - Backend Startup
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

REM Start the server
echo.
echo ==========================================
echo   Starting FastAPI Server on port 8000
echo   API Docs: http://localhost:8000/docs
echo ==========================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
