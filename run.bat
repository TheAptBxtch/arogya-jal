@echo off
REM ArogyaJal Predictive Maintenance System - Quick Run Script for Windows

echo 🚀 ArogyaJal Predictive Maintenance System
echo ==========================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found

:menu
echo.
echo Please choose an option:
echo 1) Setup environment (install dependencies)
echo 2) Run application
echo 3) Quick start (setup + run)
echo 4) Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto run
if "%choice%"=="3" goto quickstart
if "%choice%"=="4" goto exit
echo ❌ Invalid choice. Please try again.
goto menu

:setup
echo.
echo 🔧 Setting up environment...
python setup.py
echo.
echo ✅ Setup completed!
pause
goto menu

:run
echo.
echo 🌐 Starting Streamlit application...
echo 📱 The app will open in your browser at http://localhost:8501
echo 🛑 Press Ctrl+C to stop the application
echo.
streamlit run app.py
goto menu

:quickstart
echo.
echo 🔧 Setting up environment...
python setup.py
echo.
echo 🎯 Setup completed! Starting application...
streamlit run app.py
goto menu

:exit
echo.
echo 👋 Goodbye!
pause
exit /b 0