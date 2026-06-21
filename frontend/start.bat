@echo off
REM AI Stock Analyzer - Frontend Startup Script for Windows

echo ==========================================
echo   AI Stock Analyzer - Frontend Startup
echo ==========================================
echo.

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH.
    echo Please install Node.js 18+ from https://nodejs.org
    pause
    exit /b 1
)

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing dependencies...
    npm install --no-audit --no-fund
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Build the frontend
echo Building frontend...
npm run build
if errorlevel 1 (
    echo ERROR: Build failed.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   Frontend built successfully!
echo   Output: .\dist\
echo   You can serve it with any static server
echo ==========================================
echo.

REM Optionally serve with a simple HTTP server
echo Starting preview server on port 3000...
python -m http.server 3000 --directory dist

pause
