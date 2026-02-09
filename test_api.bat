@echo off
REM Video Transcoder API Testing Script for Windows

echo.
echo ========================================
echo   Video Transcoder API Test Suite
echo ========================================
echo.

set API_BASE=http://localhost:5000/api

REM Check if curl is available
curl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] curl is not installed or not in PATH!
    echo.
    echo Please install curl:
    echo - Windows 10/11: Already included
    echo - Using Chocolatey: choco install curl
    echo - Using Scoop: scoop install curl
    pause
    exit /b 1
)

echo.
echo 1. Testing GET /api/status
echo ========================================
curl -s %API_BASE%/status
echo.
echo.

echo 2. Testing GET /api/settings
echo ========================================
curl -s %API_BASE%/settings
echo.
echo.

echo 3. Testing POST /api/settings
echo ========================================
curl -s -X POST %API_BASE%/settings ^
  -H "Content-Type: application/json" ^
  -d "{\"source_folder\": \"C:\\videos\\source\", \"output_folder\": \"C:\\videos\\output\", \"watch_enabled\": false, \"output_format\": \"mp4\", \"video_codec\": \"libx264\", \"audio_codec\": \"aac\", \"preset\": \"medium\", \"crf\": 23}"
echo.
echo.

echo 4. Testing GET /api/jobs
echo ========================================
curl -s %API_BASE%/jobs
echo.
echo.

echo 5. Testing GET /api/jobs?status=completed
echo ========================================
curl -s "%API_BASE%/jobs?status=completed"
echo.
echo.

echo 6. Testing POST /api/scan
echo ========================================
curl -s -X POST %API_BASE%/scan
echo.
echo.

echo ========================================
echo API tests completed!
echo ========================================
echo.
pause
