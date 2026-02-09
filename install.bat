@echo off
setlocal enabledelayedexpansion
REM Video Transcoder - Windows One-Click Installer

title Video Transcoder Setup

color 0A
echo.
echo ========================================
echo    VIDEO TRANSCODER SETUP
echo ========================================
echo.
echo This will install and configure the
echo Video Transcoder application.
echo.
echo Requirements:
echo  - Python 3.8 or higher
echo  - FFmpeg (will check)
echo.
pause
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    color 0C
    echo.
    echo [ERROR] Python is NOT installed!
    echo.
    echo Please install Python first:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.8 or higher
    echo 3. CHECK "Add Python to PATH" during installation
    echo 4. Run this installer again
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python is installed
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv\" (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if !errorlevel! neq 0 (
        color 0C
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Installing application dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if !errorlevel! neq 0 (
    color 0C
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Create directories
echo Creating directories...
if not exist "videos\source\" mkdir videos\source
if not exist "videos\output\" mkdir videos\output
if not exist "instance\" mkdir instance
echo [OK] Directories created
echo.

REM Create .env file
if not exist ".env" (
    echo Creating configuration file...
    copy .env.example .env >nul
    echo [OK] Configuration file created
    echo.
    echo [NOTE] You can edit .env file to customize settings
) else (
    echo [OK] Configuration file already exists
)
echo.

REM Check FFmpeg
echo Checking FFmpeg installation...
where ffmpeg >nul 2>&1
if !errorlevel! neq 0 (
    color 0E
    echo.
    echo ========================================
    echo [WARNING] FFmpeg is NOT installed!
    echo ========================================
    echo.
    echo FFmpeg is REQUIRED for video transcoding.
    echo.
    echo Quick Install Options:
    echo.
    echo 1. Using Chocolatey:
    echo    choco install ffmpeg
    echo.
    echo 2. Using Scoop:
    echo    scoop install ffmpeg
    echo.
    echo 3. Using winget:
    echo    winget install Gyan.FFmpeg
    echo.
    echo 4. Manual:
    echo    https://www.gyan.dev/ffmpeg/builds/
    echo.
    echo ========================================
    echo.
    set /p install_anyway="Continue without FFmpeg? (y/n): "
    if /i not "%install_anyway%"=="y" (
        echo.
        echo Please install FFmpeg and run this installer again.
        echo.
        pause
        deactivate
        exit /b 1
    )
    color 0A
) else (
    echo [OK] FFmpeg is installed
)
echo.

REM Create desktop shortcut
echo Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT=%DESKTOP%\Video Transcoder.url
set SCRIPT_DIR=%CD%

(
    echo [InternetShortcut]
    echo URL=http://localhost:5000
    echo IconIndex=0
    echo IconFile=%SystemRoot%\System32\shell32.dll
) > "%SHORTCUT%"

echo [OK] Desktop shortcut created
echo.

REM Deactivate venv
deactivate

color 0A
echo.
echo ========================================
echo    INSTALLATION COMPLETE!
echo ========================================
echo.
echo To start the application:
echo.
echo   1. Double-click: start.bat
echo   
echo   2. Or run in Command Prompt:
echo      start.bat
echo.
echo The web interface will open at:
echo   http://localhost:5000
echo.
echo A shortcut has been created on your Desktop.
echo.
echo ========================================
echo.
set /p launch="Launch Video Transcoder now? (y/n): "
if /i "%launch%"=="y" (
    echo.
    echo Starting Video Transcoder...
    echo.
    start.bat
) else (
    echo.
    echo You can start it later by running: start.bat
    echo.
    pause
)

endlocal
