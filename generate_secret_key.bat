@echo off
REM SECRET_KEY Generator for Windows

title Generate SECRET_KEY

echo.
echo ========================================
echo    SECRET_KEY Generator
echo ========================================
echo.
echo This will generate a secure random key
echo for your .env file.
echo.
pause
echo.

python -c "import secrets; print('Your SECRET_KEY:'); print(''); print(secrets.token_hex(32))"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to generate key
    echo Make sure Python is installed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instructions:
echo ========================================
echo.
echo 1. Copy the key above
echo 2. Open .env file in a text editor
echo 3. Find the line: SECRET_KEY=your-secret-key-change-me-in-production
echo 4. Replace it with: SECRET_KEY=<your-copied-key>
echo 5. Save the .env file
echo 6. Restart the application
echo.
echo ========================================
echo.
pause
