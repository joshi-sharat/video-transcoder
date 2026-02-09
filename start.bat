@echo off
echo.
echo ========================================
echo    Video Transcoder - Starting...
echo ========================================
echo.

REM Check Python
echo Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python not found!
    echo Install from: https://www.python.org/
    pause
    exit /b 1
)
echo OK - Python found
echo.

REM Create venv if needed
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create venv
        pause
        exit /b 1
    )
    echo OK - Virtual environment created
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate venv
    pause
    exit /b 1
)
echo OK - Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies (this may take a minute)...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo OK - Dependencies installed
echo.

REM Create folders
if not exist videos\source mkdir videos\source
if not exist videos\output mkdir videos\output
if not exist instance mkdir instance

REM Create .env
if not exist .env (
    copy .env.example .env >nul 2>&1
)

REM Start the app
echo.
echo ========================================
echo Starting Video Transcoder...
echo ========================================
echo.
echo Web interface: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

echo.
echo Server stopped.
pause