@echo off
REM ArogyaJal - Click to Start (NO installation needed!)

echo.
echo ================================================================
echo      ArogyaJal Predictive Maintenance System
echo ================================================================
echo      ZERO Dependencies - NO pip installs needed!
echo ================================================================
echo.

REM Check if Python exists
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo.
    echo 💡 OPTION 1: Install Python from https://www.python.org/downloads/
    echo.
    echo 💡 OPTION 2: Just open "index.html" in your browser!
    echo    ^(Double-click index.html - works without Python^)
    echo.
    pause
    exit /b 1
)

echo ✅ Python found - Starting server...
echo.

REM Run the app
python run_app.py

pause