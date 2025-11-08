@echo off
REM ArogyaJal Easy Run for Windows - Bypasses all installation issues

echo 🚀 ArogyaJal Predictive Maintenance System
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not found. Please install Python 3.7+ first.
    echo 💡 Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python found

REM Try to install streamlit with multiple methods
echo.
echo 🔧 Installing Streamlit (this may take a minute)...

REM Method 1: Standard pip
pip install streamlit >nul 2>&1
if %errorlevel% equ 0 goto test_streamlit

REM Method 2: User installation
pip install --user streamlit >nul 2>&1
if %errorlevel% equ 0 goto test_streamlit

REM Method 3: No cache
pip install --no-cache-dir streamlit >nul 2>&1
if %errorlevel% equ 0 goto test_streamlit

REM Method 4: Specific version
pip install streamlit==1.28.1 >nul 2>&1
if %errorlevel% equ 0 goto test_streamlit

REM Method 5: Python module
python -m pip install streamlit >nul 2>&1
if %errorlevel% equ 0 goto test_streamlit

echo ❌ Failed to install Streamlit automatically
echo.
echo 💡 Please try manual installation:
echo    1. Open Command Prompt as Administrator
echo    2. Run: pip install streamlit
echo    3. If that fails, try: pip install --user streamlit
echo.
echo Or download from: https://docs.streamlit.io/knowledge-base/tutorials/installation
echo.
pause
exit /b 1

:test_streamlit
echo ✅ Streamlit installed successfully

REM Create data directory
if not exist "data" mkdir data
echo ✅ Created data directory

REM Run the application
echo.
echo 🌐 Starting ArogyaJal Application...
echo 📱 Opening browser at http://localhost:8501
echo 🛑 Press Ctrl+C to stop the application
echo.
echo 💡 If browser doesn't open automatically, visit: http://localhost:8501
echo.

REM Try different run methods
streamlit run simple_app.py >nul 2>&1
if %errorlevel% equ 0 goto end

python -m streamlit run simple_app.py
if %errorlevel% equ 0 goto end

echo ❌ Failed to start Streamlit
echo 💡 Please try running manually:
echo    streamlit run simple_app.py
echo.
pause

:end
echo.
echo 👋 Thank you for using ArogyaJal!
pause