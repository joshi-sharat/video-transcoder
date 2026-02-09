# Video Transcoder Startup Script for Windows (PowerShell)

Write-Host ""
Write-Host "========================================"
Write-Host "   Video Transcoder Startup"
Write-Host "========================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "[OK] Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to activate virtual environment" -ForegroundColor Red
    Write-Host ""
    Write-Host "If you get an execution policy error, run:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] Virtual environment activated" -ForegroundColor Green

Write-Host ""

# Install/update dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] Dependencies installed" -ForegroundColor Green

Write-Host ""

# Create necessary directories
$directories = @("videos\source", "videos\output", "instance")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "[OK] Directories created" -ForegroundColor Green

Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[WARNING] Please edit .env file with your settings" -ForegroundColor Yellow
}

Write-Host ""

# Check if FFmpeg is installed
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-String "ffmpeg version"
    Write-Host "[OK] FFmpeg found: $ffmpegVersion" -ForegroundColor Green
} catch {
    Write-Host "========================================"
    Write-Host "[WARNING] FFmpeg is not installed!" -ForegroundColor Yellow
    Write-Host "========================================"
    Write-Host ""
    Write-Host "FFmpeg is required for video transcoding."
    Write-Host ""
    Write-Host "Installation options:"
    Write-Host ""
    Write-Host "1. Using Chocolatey (recommended):" -ForegroundColor Cyan
    Write-Host "   choco install ffmpeg"
    Write-Host ""
    Write-Host "2. Using Scoop:" -ForegroundColor Cyan
    Write-Host "   scoop install ffmpeg"
    Write-Host ""
    Write-Host "3. Using winget (Windows 10/11):" -ForegroundColor Cyan
    Write-Host "   winget install Gyan.FFmpeg"
    Write-Host ""
    Write-Host "4. Manual installation:" -ForegroundColor Cyan
    Write-Host "   - Download from: https://www.gyan.dev/ffmpeg/builds/"
    Write-Host "   - Extract and add to PATH"
    Write-Host ""
    Write-Host "========================================"
    Write-Host ""

    $continue = Read-Host "Continue without FFmpeg? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Please install FFmpeg and run this script again."
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "========================================"
Write-Host "Starting Video Transcoder..."
Write-Host "========================================"
Write-Host ""
Write-Host "Web interface will be available at:"
Write-Host "http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""

# Start the application
python app.py

# Deactivate virtual environment on exit
deactivate