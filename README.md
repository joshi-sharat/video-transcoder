# 🎬 Video Transcoder Web Application

A powerful web-based video transcoding application with automatic folder monitoring, built with Flask and FFmpeg.

## ✨ Features

- **Web-based Interface**: Easy-to-use dashboard for managing video transcoding jobs
- **RESTful API**: Complete API for programmatic access
- **Auto-watching**: Automatically detect and transcode new videos added to source folder
- **Multiple Formats**: Support for MP4, MKV, WebM, AVI, and more
- **Codec Options**: H.264, H.265, VP9, AAC, MP3, Opus
- **Quality Control**: Adjustable CRF (Constant Rate Factor) for quality vs file size
- **Real-time Progress**: Live progress tracking for all transcoding jobs
- **Job Management**: View, filter, and manage all transcoding jobs
- **System Monitoring**: CPU and memory usage tracking
- **🤖 RAG Integration**: Query external RAG (Retrieval Augmented Generation) services
- **Docker Support**: Easy deployment with Docker and Docker Compose

## 📋 Requirements

- Python 3.8+
- FFmpeg installed on your system
- Linux environment (tested on Ubuntu)

## 🚀 Quick Start

### Option 1: Linux/Mac Installation

1. **Clone or download the repository**

2. **Install system dependencies**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg python3-pip python3-venv

# Fedora/RHEL
sudo dnf install ffmpeg python3-pip

# Arch Linux
sudo pacman -S ffmpeg python-pip

# macOS (using Homebrew)
brew install ffmpeg python
```

3. **Run the startup script**:
```bash
chmod +x start.sh
./start.sh
```

4. **Access the web interface**:
Open your browser and navigate to `http://localhost:5000`

### Option 1B: Windows Installation

**Quick Install (Recommended):**

1. **Double-click `install.bat`** - This will:
   - Check Python installation
   - Create virtual environment
   - Install all dependencies
   - Check for FFmpeg
   - Create desktop shortcut

2. **Run the application:**
   - Double-click `start.bat`
   - Or in Command Prompt: `start.bat`

3. **Access the web interface:**
   - Open browser: `http://localhost:5000`

**See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed Windows instructions.**

### Manual Installation (All Platforms)

1. **Create and activate virtual environment**:
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create necessary directories**:
```bash
# Linux/Mac
mkdir -p videos/source videos/output

# Windows
mkdir videos\source videos\output
```

4. **Run the application**:
```bash
python app.py
```

5. **Access the web interface**:
Open your browser and navigate to `http://localhost:5000`

### Option 2: Docker Installation

1. **Make sure Docker and Docker Compose are installed**

2. **Create video directories**:
```bash
mkdir -p videos/source videos/output
```

3. **Build and run with Docker Compose**:
```bash
docker-compose up -d
```

4. **Access the web interface**:
Open your browser and navigate to `http://localhost:5000`

5. **View logs**:
```bash
docker-compose logs -f
```

6. **Stop the application**:
```bash
docker-compose down
```

## 🎯 Usage

### Web Interface

1. **Configure Settings**:
   - Set your source folder path (where original videos are located)
   - Set your output folder path (where transcoded videos will be saved)
   - Choose output format (MP4, MKV, WebM, AVI)
   - Select video codec (H.264, H.265, VP9)
   - Select audio codec (AAC, MP3, Opus)
   - Adjust encoding preset (faster = lower quality, slower = better quality)
   - Set CRF value (0-51, lower = better quality, higher = smaller file)
   - Enable auto-watch to automatically transcode new files

2. **Scan for Videos**:
   - Click "Scan for New Videos" to find all videos in your source folder
   - New transcode jobs will be created automatically

3. **Monitor Progress**:
   - View all jobs in the jobs list
   - Filter by status: All, Pending, Processing, Completed, Failed
   - See real-time progress for active transcoding jobs
   - Check system resource usage (CPU and Memory)

4. **Manage Jobs**:
   - Delete completed or failed jobs
   - View error messages for failed jobs

### 🤖 RAG Integration

Query external RAG (Retrieval Augmented Generation) services directly from the interface.

**Quick Start:**

1. **Configure RAG Service** (in `.env`):
   ```env
   RAG_URL=localhost
   RAG_PORT=8000
   RAG_ENDPOINT=/api/query
   ```

2. **Start Mock RAG Service** (for testing):
   ```bash
   python mock_rag_service.py
   ```

3. **Access RAG Interface**:
   - Click "🤖 RAG Query" in the header
   - Or navigate to: http://localhost:5000/rag

4. **Submit Queries**:
   - Enter your query
   - Adjust parameters (top_k, temperature)
   - Get instant responses

**API Usage:**
```bash
curl -X POST http://localhost:5000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate Yoga Class", "top_k": 3, "use_rag": true, "temperature": 0.1}'
```

See [RAG_INTEGRATION.md](RAG_INTEGRATION.md) for complete documentation.

### API Endpoints

#### Get Settings
```bash
GET /api/settings
```

#### Update Settings
```bash
POST /api/settings
Content-Type: application/json

{
  "source_folder": "/path/to/source",
  "output_folder": "/path/to/output",
  "watch_enabled": true,
  "output_format": "mp4",
  "video_codec": "libx264",
  "audio_codec": "aac",
  "preset": "medium",
  "crf": 23
}
```

#### Get All Jobs
```bash
GET /api/jobs
GET /api/jobs?status=completed
```

#### Get Specific Job
```bash
GET /api/jobs/<job_id>
```

#### Create Manual Job
```bash
POST /api/jobs
Content-Type: application/json

{
  "source_file": "/path/to/video.mp4"
}
```

#### Delete Job
```bash
DELETE /api/jobs/<job_id>
```

#### Scan Source Folder
```bash
POST /api/scan
```

#### Get System Status
```bash
GET /api/status
```

## 📁 Project Structure

```
video-transcoder/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .env.example          # Environment variables template
├── app/
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Application configuration
│   ├── transcoder.py     # Video transcoding logic
│   └── watcher.py        # Folder monitoring logic
├── templates/
│   └── index.html        # Web interface template
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── app.js        # Frontend JavaScript
└── videos/
    ├── source/           # Source video folder
    └── output/           # Transcoded video folder
```

## ⚙️ Configuration

### Encoding Presets

- **ultrafast** - Fastest encoding, largest file size
- **superfast**
- **veryfast**
- **faster**
- **fast**
- **medium** - Default, good balance
- **slow**
- **slower**
- **veryslow** - Slowest encoding, smallest file size

### CRF Values

- **0-17** - Visually lossless (very large files)
- **18-23** - High quality (recommended range)
- **24-28** - Medium quality
- **29-51** - Low quality (small files)

Recommended: **23** for most use cases

### Video Codecs

- **H.264 (libx264)** - Best compatibility, good quality
- **H.265 (libx265)** - Better compression, newer devices
- **VP9** - Open source, good for web
- **copy** - No re-encoding (fast, preserves quality)

### Audio Codecs

- **AAC** - Best compatibility, good quality
- **MP3** - Universal compatibility
- **Opus** - Best quality for same bitrate
- **copy** - No re-encoding (fast, preserves quality)

## 🔧 Troubleshooting

### FFmpeg not found
Make sure FFmpeg is installed and in your system PATH:
```bash
which ffmpeg
ffmpeg -version
```

### Permission denied on folders
Ensure the application has read/write permissions:
```bash
chmod -R 755 videos/
```

### Port 5000 already in use
Change the port in `app.py` or use environment variable:
```bash
PORT=8000 python app.py
```

### Docker container won't start
Check logs for errors:
```bash
docker-compose logs web
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Video processing powered by [FFmpeg](https://ffmpeg.org/)
- Folder monitoring with [Watchdog](https://github.com/gorakhargosh/watchdog)

## 📞 Support

If you encounter any issues or have questions, please open an issue on the project repository.

---

**Enjoy transcoding! 🎥✨**
