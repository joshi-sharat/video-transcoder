# Video Transcoder Project - Quick Start Guide

## 📦 What You Got

A complete video transcoding web application with:

✅ Flask web server with REST API
✅ Modern, responsive web interface
✅ Automatic folder monitoring
✅ FFmpeg-powered video transcoding
✅ Docker support for easy deployment
✅ SQLite database for job tracking
✅ Real-time progress monitoring
✅ System resource monitoring

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies

```bash
cd video-transcoder
chmod +x start.sh
./start.sh
```

The script will:
- Create a Python virtual environment
- Install all dependencies
- Check for FFmpeg
- Start the application

### 2. Access the Web Interface

Open your browser and go to:
```
http://localhost:5000
```

### 3. Configure and Start Transcoding

In the web interface:
1. Set your source folder (where original videos are)
2. Set your output folder (where transcoded videos will go)
3. Choose your encoding settings
4. Click "Scan for New Videos" or enable auto-watch

## 🐳 Alternative: Docker

If you prefer Docker:

```bash
cd video-transcoder
docker-compose up -d
```

Then access: http://localhost:5000

## 📁 Project Files

```
video-transcoder/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── start.sh                  # Quick start script
├── test_api.sh              # API testing script
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose config
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── video-transcoder.service # Systemd service file
├── README.md                # Full documentation
├── app/
│   ├── config.py           # App configuration
│   ├── transcoder.py       # Transcoding engine
│   └── watcher.py          # Folder monitoring
├── templates/
│   └── index.html          # Web interface
├── static/
│   ├── css/style.css       # Styles
│   └── js/app.js           # Frontend logic
└── videos/
    ├── source/             # Put source videos here
    └── output/             # Transcoded videos go here
```

## 🎯 Main Features

### Web Interface
- Configure source/output folders
- Choose video/audio codecs
- Adjust quality settings (CRF)
- Select encoding preset
- Enable auto-watch mode
- View all jobs with status
- Real-time progress bars
- System monitoring (CPU/Memory)

### API Endpoints
- `GET /api/settings` - Get current settings
- `POST /api/settings` - Update settings
- `GET /api/jobs` - List all jobs
- `GET /api/jobs?status=completed` - Filter jobs
- `POST /api/jobs` - Create manual job
- `DELETE /api/jobs/<id>` - Delete job
- `POST /api/scan` - Scan for new videos
- `GET /api/status` - System status

### Supported Formats
- **Input**: MP4, AVI, MKV, MOV, FLV, WMV, M4V, WebM, MPG, MPEG
- **Output**: MP4, MKV, WebM, AVI
- **Video Codecs**: H.264, H.265, VP9
- **Audio Codecs**: AAC, MP3, Opus

## 🔧 Testing the API

Run the test script:
```bash
./test_api.sh
```

Or test manually:
```bash
# Get status
curl http://localhost:5000/api/status

# Get settings
curl http://localhost:5000/api/settings

# Update settings
curl -X POST http://localhost:5000/api/settings \
  -H "Content-Type: application/json" \
  -d '{"source_folder": "/path/to/videos", "output_folder": "/path/to/output"}'

# Scan for videos
curl -X POST http://localhost:5000/api/scan
```

## 📝 Configuration Tips

### Quality Settings (CRF)
- 18-23: High quality (recommended)
- 23-28: Medium quality
- 28+: Lower quality, smaller files

### Encoding Presets
- Fast presets: Larger files, faster encoding
- Slow presets: Smaller files, better quality, slower encoding
- **medium**: Good balance (default)

### Auto-watch Mode
When enabled, automatically transcodes any new video files added to the source folder.

## 🚀 Production Deployment

### Using Systemd (Linux)

1. Copy the project to `/opt/video-transcoder`
2. Install the service:
```bash
sudo cp video-transcoder.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable video-transcoder
sudo systemctl start video-transcoder
```

3. Check status:
```bash
sudo systemctl status video-transcoder
```

### Using Docker in Production

Edit `docker-compose.yml` and change:
- Mount your actual video directories
- Set `DEBUG=False`
- Use a strong `SECRET_KEY`

Then:
```bash
docker-compose up -d
```

## 🆘 Troubleshooting

**FFmpeg not found?**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# Fedora/RHEL
sudo dnf install ffmpeg
```

**Permission errors?**
```bash
chmod -R 755 videos/
```

**Port 5000 in use?**
Edit `app.py` and change the port, or:
```bash
PORT=8000 python app.py
```

**Need help?**
Check the full README.md for detailed documentation.

## 📊 What Happens When You Transcode?

1. You configure source and output folders
2. Click "Scan" or enable auto-watch
3. App finds all video files
4. Creates transcode jobs in database
5. Processes jobs one by one with FFmpeg
6. Shows real-time progress
7. Saves transcoded files to output folder
8. Updates job status to "completed"

## 🎉 You're Ready!

Everything is set up and ready to go. Just run `./start.sh` and start transcoding!

For full documentation, see README.md
