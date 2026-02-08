#!/bin/bash

# Video Transcoder Startup Script

echo "🎬 Starting Video Transcoder..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p videos/source videos/output instance

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your settings"
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg is not installed!"
    echo "Please install FFmpeg before running the application."
    echo ""
    echo "Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "Fedora/RHEL: sudo dnf install ffmpeg"
    echo "Arch Linux: sudo pacman -S ffmpeg"
    exit 1
fi

echo "✅ FFmpeg found: $(ffmpeg -version | head -n 1)"
echo ""
echo "Starting application..."
echo "Web interface will be available at: http://localhost:5000"
echo ""

# Run the application
python app.py
