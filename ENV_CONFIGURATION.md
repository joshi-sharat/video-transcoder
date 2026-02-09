# 🔧 Environment Configuration Guide

## What is the .env file?

The `.env` file stores configuration settings for your Video Transcoder application. It keeps sensitive information (like secret keys) and custom settings separate from your code.

## 📁 File Location

```
video-transcoder/
├── .env.example    ← Template file (included in project)
└── .env            ← Your actual config (created from .env.example)
```

**Important:** 
- `.env.example` is the template (checked into git)
- `.env` is your personal config (NOT checked into git - it's in .gitignore)

## 🚀 Quick Setup

### **Automatic Setup (Recommended)**

When you run `install.bat` or `start.bat` (Windows) or `start.sh` (Linux/Mac), the `.env` file is automatically created from `.env.example`.

### **Manual Setup**

**Windows (Command Prompt):**
```cmd
copy .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

## 📝 Configuration Options

### **Essential Settings**

#### 1. Secret Key
```env
SECRET_KEY=your-secret-key-change-me-in-production
```

**What it does:** Secures Flask sessions and cookies  
**For development:** Can leave as default  
**For production:** MUST change to a random string

**Generate a secure key:**

```python
# Run this in Python to generate a random key
import secrets
print(secrets.token_hex(32))
```

Or use online generator: https://randomkeygen.com/

#### 2. Debug Mode
```env
DEBUG=True
```

**What it does:** 
- `True` = Development mode (detailed errors, auto-reload)
- `False` = Production mode (hide errors from users)

**When to use:**
- Development: `DEBUG=True`
- Production: `DEBUG=False`

#### 3. Server Settings
```env
HOST=0.0.0.0
PORT=5000
```

**HOST options:**
- `0.0.0.0` = Accept connections from any IP (allows remote access)
- `127.0.0.1` = Only local connections (more secure)

**PORT:**
- Default: `5000`
- Change if port is in use: `8000`, `8080`, etc.

### **FFmpeg Configuration**

#### Default (FFmpeg in PATH):
```env
FFMPEG_PATH=ffmpeg
FFPROBE_PATH=ffprobe
```

#### Windows (Custom Path):
```env
FFMPEG_PATH=C:/ffmpeg/bin/ffmpeg.exe
FFPROBE_PATH=C:/ffmpeg/bin/ffprobe.exe
```

#### Linux (Custom Path):
```env
FFMPEG_PATH=/usr/local/bin/ffmpeg
FFPROBE_PATH=/usr/local/bin/ffprobe
```

### **Database Configuration**

#### Default (SQLite in project folder):
```env
DATABASE_URL=sqlite:///transcoder.db
```

#### Custom Location (Windows):
```env
DATABASE_URL=sqlite:///C:/Users/YourName/AppData/transcoder.db
```

#### Custom Location (Linux):
```env
DATABASE_URL=sqlite:////var/lib/video-transcoder/transcoder.db
```

**Note:** SQLite URLs use 3 slashes for relative paths, 4 for absolute on Linux.

### **Default Transcoding Settings**

```env
DEFAULT_OUTPUT_FORMAT=mp4
DEFAULT_VIDEO_CODEC=libx264
DEFAULT_AUDIO_CODEC=aac
DEFAULT_PRESET=medium
DEFAULT_CRF=23
```

**Output Formats:**
- `mp4` - Best compatibility
- `mkv` - Best features
- `webm` - Web optimized
- `avi` - Legacy support

**Video Codecs:**
- `libx264` - H.264 (best compatibility)
- `libx265` - H.265 (better compression, slower)
- `libvpx-vp9` - VP9 (web optimized)

**Audio Codecs:**
- `aac` - Best compatibility
- `libmp3lame` - MP3
- `libopus` - Best quality for size

**Presets (speed vs quality):**
- `ultrafast` - Fastest, largest files
- `fast` - Fast, larger files
- `medium` - Balanced (recommended)
- `slow` - Slower, better quality
- `veryslow` - Slowest, best quality

**CRF (quality):**
- `18-23` - High quality (recommended)
- `23-28` - Medium quality
- `28+` - Lower quality, smaller files

### **Default Folder Paths**

#### Leave Empty (Configure in Web UI):
```env
DEFAULT_SOURCE_FOLDER=
DEFAULT_OUTPUT_FOLDER=
```

#### Or Set Defaults (Windows):
```env
DEFAULT_SOURCE_FOLDER=C:/Users/YourName/Videos/Source
DEFAULT_OUTPUT_FOLDER=C:/Users/YourName/Videos/Output
```

#### Or Set Defaults (Linux):
```env
DEFAULT_SOURCE_FOLDER=/home/user/videos/source
DEFAULT_OUTPUT_FOLDER=/home/user/videos/output
```

### **Auto-Watch Settings**

```env
DEFAULT_WATCH_ENABLED=false
```

**Options:**
- `true` - Automatically transcode new files
- `false` - Manual scanning only

## 📋 Complete Example Configurations

### **Development Setup (Windows)**

```env
# Development Configuration
SECRET_KEY=dev-key-not-for-production
DEBUG=True
HOST=127.0.0.1
PORT=5000
DATABASE_URL=sqlite:///transcoder.db
FFMPEG_PATH=ffmpeg
FFPROBE_PATH=ffprobe
DEFAULT_OUTPUT_FORMAT=mp4
DEFAULT_VIDEO_CODEC=libx264
DEFAULT_AUDIO_CODEC=aac
DEFAULT_PRESET=medium
DEFAULT_CRF=23
DEFAULT_SOURCE_FOLDER=C:/Users/YourName/Videos/Source
DEFAULT_OUTPUT_FOLDER=C:/Users/YourName/Videos/Output
DEFAULT_WATCH_ENABLED=false
```

### **Development Setup (Linux)**

```env
# Development Configuration
SECRET_KEY=dev-key-not-for-production
DEBUG=True
HOST=127.0.0.1
PORT=5000
DATABASE_URL=sqlite:///transcoder.db
FFMPEG_PATH=/usr/bin/ffmpeg
FFPROBE_PATH=/usr/bin/ffprobe
DEFAULT_OUTPUT_FORMAT=mp4
DEFAULT_VIDEO_CODEC=libx264
DEFAULT_AUDIO_CODEC=aac
DEFAULT_PRESET=medium
DEFAULT_CRF=23
DEFAULT_SOURCE_FOLDER=/home/user/videos/source
DEFAULT_OUTPUT_FOLDER=/home/user/videos/output
DEFAULT_WATCH_ENABLED=false
```

### **Production Setup**

```env
# Production Configuration
SECRET_KEY=9f8d7a6b5c4e3d2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8
DEBUG=False
HOST=0.0.0.0
PORT=5000
DATABASE_URL=sqlite:////var/lib/video-transcoder/transcoder.db
FFMPEG_PATH=/usr/bin/ffmpeg
FFPROBE_PATH=/usr/bin/ffprobe
DEFAULT_OUTPUT_FORMAT=mp4
DEFAULT_VIDEO_CODEC=libx264
DEFAULT_AUDIO_CODEC=aac
DEFAULT_PRESET=slow
DEFAULT_CRF=20
DEFAULT_WATCH_ENABLED=true
LOG_LEVEL=WARNING
```

## 🔒 Security Best Practices

### **Development:**
✅ Use simple secret key  
✅ Keep DEBUG=True  
✅ Use 127.0.0.1 for HOST  
✅ Keep .env file local (never commit)

### **Production:**
✅ Generate strong random secret key  
✅ Set DEBUG=False  
✅ Use proper firewall rules  
✅ Set up HTTPS  
✅ Regular backups of database

## ⚠️ Important Notes

1. **Never commit .env to git**
   - The `.gitignore` file already excludes it
   - Only commit `.env.example`

2. **Restart required**
   - Changes to `.env` require restarting the app
   - Stop with Ctrl+C, then run `start.bat` again

3. **Paths on Windows**
   - Use forward slashes: `C:/path/to/folder`
   - Or double backslashes: `C:\\path\\to\\folder`
   - Avoid single backslashes

4. **Empty values**
   - Leave blank for optional settings
   - Don't use quotes unless needed

5. **Comments**
   - Lines starting with `#` are comments
   - Use for documentation

## 🛠️ Troubleshooting

### **App doesn't start after changing .env:**

1. **Check syntax:**
   - No spaces around `=`
   - Correct format: `KEY=value`
   - Not: `KEY = value`

2. **Check paths:**
   - Make sure folders exist
   - Use correct path format for your OS

3. **Check quotes:**
   - Usually not needed
   - If path has spaces, use: `PATH="C:/My Folder/Videos"`

4. **Verify FFmpeg paths:**
   ```cmd
   # Test if path works
   ffmpeg -version
   ```

5. **Check for typos:**
   - Variable names are case-sensitive
   - `DEBUG=True` not `debug=true`

### **Settings not taking effect:**

1. Restart the application
2. Check you edited `.env` not `.env.example`
3. Verify .env is in the project root folder

### **Can't find .env file:**

Files starting with `.` are hidden on some systems:

**Windows:**
- Enable "Show hidden files" in File Explorer
- View → Options → View tab → Show hidden files

**Linux/Mac:**
```bash
ls -la  # Shows hidden files
```

## ✅ Verification Checklist

- [ ] `.env` file created from `.env.example`
- [ ] Secret key changed (if production)
- [ ] Debug mode set correctly
- [ ] FFmpeg paths configured
- [ ] Folder paths set (optional)
- [ ] File is in project root directory
- [ ] Application restarted after changes

## 📚 Related Files

- `.env.example` - Template (this is what you copy)
- `.env` - Your actual config
- `app/config.py` - Reads these settings
- `.gitignore` - Excludes .env from git

---

**Ready to start?** Just run `start.bat` (Windows) or `./start.sh` (Linux/Mac) - the .env file will be created automatically!
