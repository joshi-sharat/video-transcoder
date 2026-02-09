@echo off
echo.
echo ========================================
echo   Folder Structure Check
echo ========================================
echo.

set ERROR_FOUND=0

REM Check templates folder
if not exist "templates\" (
    echo [ERROR] templates\ folder is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] templates\ folder exists
)

REM Check templates/index.html
if not exist "templates\index.html" (
    echo [ERROR] templates\index.html is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] templates\index.html exists
)

REM Check static folder
if not exist "static\" (
    echo [ERROR] static\ folder is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] static\ folder exists
)

REM Check static/css
if not exist "static\css\" (
    echo [ERROR] static\css\ folder is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] static\css\ folder exists
)

REM Check static/css/style.css
if not exist "static\css\style.css" (
    echo [ERROR] static\css\style.css is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] static\css\style.css exists
)

REM Check static/js
if not exist "static\js\" (
    echo [ERROR] static\js\ folder is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] static\js\ folder exists
)

REM Check static/js/app.js
if not exist "static\js\app.js" (
    echo [ERROR] static\js\app.js is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] static\js\app.js exists
)

REM Check app folder
if not exist "app\" (
    echo [ERROR] app\ folder is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] app\ folder exists
)

REM Check app files
if not exist "app\__init__.py" (
    echo [ERROR] app\__init__.py is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] app\__init__.py exists
)

if not exist "app\config.py" (
    echo [ERROR] app\config.py is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] app\config.py exists
)

if not exist "app\transcoder.py" (
    echo [ERROR] app\transcoder.py is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] app\transcoder.py exists
)

if not exist "app\watcher.py" (
    echo [ERROR] app\watcher.py is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] app\watcher.py exists
)

REM Check main files
if not exist "app.py" (
    echo [ERROR] app.py is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] app.py exists
)

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt is missing!
    set ERROR_FOUND=1
) else (
    echo [OK] requirements.txt exists
)

echo.
echo ========================================
if %ERROR_FOUND%==1 (
    echo [ERROR] Some files or folders are missing!
    echo.
    echo This usually means:
    echo 1. The ZIP file was not extracted completely
    echo 2. Files were extracted to the wrong location
    echo 3. Files were moved or deleted
    echo.
    echo SOLUTION:
    echo 1. Re-extract the video-transcoder.zip file
    echo 2. Make sure ALL folders are extracted
    echo 3. Run this script again from the extracted folder
    echo.
    echo Expected structure:
    echo video-transcoder\
    echo   ^|-- app\
    echo   ^|-- templates\
    echo   ^|-- static\
    echo   ^|-- app.py
    echo   ^|-- requirements.txt
    echo   ^|-- start.bat
    echo.
) else (
    echo [SUCCESS] All files and folders are in place!
    echo You can now run: start.bat
    echo.
)
echo ========================================
echo.
pause
