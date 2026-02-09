@echo off
echo.
echo ========================================
echo    Video Transcoder - Starting...
echo ========================================
echo.

REM Check folder structure first
echo Checking folder structure...
if not exist "templates\index.html" (
    echo.
    echo ========================================
    echo [ERROR] templates\index.html not found!
    echo ========================================
    echo.
    echo This means the project was not extracted correctly.
    echo.
    echo SOLUTION:
    echo 1. Re-extract video-transcoder.zip completely
    echo 2. Make sure you extract ALL folders
    echo 3. Your current folder should contain:
    echo    - templates\ folder with index.html
    echo    - static\ folder with css\ and js\
    echo    - app\ folder with Python files
    echo    - app.py and requirements.txt
    echo.
    echo You can run check-structure.bat to see what's missing
    echo.
    pause
    exit /b 1
)

if not exist "static\css\style.css" (
    echo.
    echo [ERROR] static\css\style.css not found!
    echo Please re-extract the ZIP file completely.
    echo.
    pause
    exit /b 1
)

if not exist "app\config.py" (
    echo.
    echo [ERROR] app\config.py not found!
    echo Please re-extract the ZIP file completely.
    echo.
    pause
    exit /b 1
)

echo [OK] Folder structure is correct
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
echo [OK] Python found
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
    echo [OK] Virtual environment created
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate venv
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies (this may take a minute)...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo [OK] Dependencies installed
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
