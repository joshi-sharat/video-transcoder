# 🪟 Windows Setup Guide - Video Transcoder

Complete guide for setting up and running the Video Transcoder on Windows.

## 📋 Prerequisites

### 1. Python Installation

**Download and Install Python:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or higher (latest recommended)
3. **IMPORTANT**: Check ✅ "Add Python to PATH" during installation
4. Click "Install Now"

**Verify Installation:**
```cmd
python --version
```

Should show: `Python 3.x.x`

### 2. FFmpeg Installation

FFmpeg is required for video transcoding. Choose one method:

#### Option A: Using Chocolatey (Recommended)

1. Install Chocolatey (if not installed):
   - Open PowerShell as Administrator
   - Run:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. Install FFmpeg:
   ```cmd
   choco install ffmpeg
   ```

#### Option B: Using Scoop

1. Install Scoop (if not installed):
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   irm get.scoop.sh | iex
   ```

2. Install FFmpeg:
   ```cmd
   scoop install ffmpeg
   ```

#### Option C: Using winget (Windows 10/11)

```cmd
winget install Gyan.FFmpeg
```

#### Option D: Manual Installation

1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Choose "ffmpeg-release-essentials.zip"
3. Extract to `C:\ffmpeg`
4. Add to PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" under System Variables
   - Add: `C:\ffmpeg\bin`
   - Click OK
5. Restart Command Prompt

**Verify Installation:**
```cmd
ffmpeg -version
```

## 🚀 Quick Start

### Method 1: Using Batch File (Easiest)

1. **Extract the video-transcoder.zip**
2. **Open Command Prompt** in the extracted folder:
   - Shift + Right-click in folder → "Open command window here"
   - Or: Shift + Right-click → "Open PowerShell window here"

3. **Run the startup script:**
   ```cmd
   start.bat
   ```

4. **Access the web interface:**
   - Open browser: http://localhost:5000

### Method 2: Using PowerShell

1. **Open PowerShell** in the project folder
2. **Set execution policy** (first time only):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Run the startup script:**
   ```powershell
   .\start.ps1
   ```

4. **Access the web interface:**
   - Open browser: http://localhost:5000

### Method 3: Manual Setup

1. **Create virtual environment:**
   ```cmd
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate.bat
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Create directories:**
   ```cmd
   mkdir videos\source
   mkdir videos\output
   ```

5. **Run the application:**
   ```cmd
   python app.py
   ```

6. **Access the web interface:**
   - Open browser: http://localhost:5000

## 📁 Folder Paths on Windows

When configuring folders in the web interface, use Windows paths:

**Examples:**
```
Source Folder: C:\Users\YourName\Videos\Source
Output Folder: C:\Users\YourName\Videos\Output

Or relative paths:
Source Folder: videos\source
Output Folder: videos\output
```

**Note:** Use either:
- `C:\path\to\folder` (backslashes)
- `C:/path/to/folder` (forward slashes - also works)

## 🔧 Common Issues

### Issue 1: "Python not found"

**Solution:**
1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH:
   - Find Python installation (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx`)
   - Add to PATH environment variable

### Issue 2: "ffmpeg not found"

**Solution:**
1. Install FFmpeg using one of the methods above
2. Verify with: `ffmpeg -version`
3. Restart Command Prompt after installation

### Issue 3: "Script cannot be loaded" (PowerShell)

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 4: "Permission denied" when creating folders

**Solution:**
- Run Command Prompt as Administrator
- Or choose a folder where you have write permissions

### Issue 5: Port 5000 already in use

**Solution:**
Edit `app.py` and change the port:
```python
app.run(host='0.0.0.0', port=8000, debug=True)  # Change 5000 to 8000
```

### Issue 6: Virtual environment activation fails

**Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**Git Bash:**
```bash
source venv/Scripts/activate
```

## 🐳 Docker on Windows

If you have Docker Desktop installed:

1. **Make sure Docker is running**

2. **Open PowerShell or Command Prompt** in project folder

3. **Build and run:**
   ```cmd
   docker-compose up -d
   ```

4. **Access:** http://localhost:5000

5. **Stop:**
   ```cmd
   docker-compose down
   ```

**Configure volumes** in `docker-compose.yml`:
```yaml
volumes:
  - C:\Users\YourName\Videos\source:/app/videos/source
  - C:\Users\YourName\Videos\output:/app/videos/output
```

## 📝 Testing the API

Run the test script:

**Command Prompt:**
```cmd
test_api.bat
```

**PowerShell:**
```powershell
.\test_api.bat
```

## 🛑 Stopping the Application

**In Command Prompt/PowerShell:**
- Press `Ctrl + C`
- Type `deactivate` to exit virtual environment

**If running in background:**
```cmd
taskkill /F /IM python.exe
```

## 📊 System Requirements

- **OS:** Windows 10 or higher (Windows 11 recommended)
- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB+ recommended for video transcoding)
- **Disk:** Depends on video size
- **FFmpeg:** Latest version

## 🎯 Video Format Support

**Input Formats:**
- MP4, AVI, MKV, MOV, FLV, WMV, M4V, WebM, MPG, MPEG

**Output Formats:**
- MP4, MKV, WebM, AVI

## 💡 Tips for Windows Users

1. **Use absolute paths** for source/output folders
   ```
   C:\Users\YourName\Videos\Source
   ```

2. **Firewall:** Windows may ask for firewall permission - Allow it

3. **Antivirus:** Some antivirus may flag Python scripts - Add exception

4. **Long paths:** If you get "path too long" errors:
   - Run: `reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f`
   - Restart computer

5. **Performance:** 
   - Use SSD for better performance
   - Close other heavy applications during transcoding

6. **Network folders:** Avoid using network drives for source/output
   - Copy files locally first for best performance

## 🔐 Running as Windows Service

To run as a Windows service:

1. Install NSSM (Non-Sucking Service Manager):
   ```cmd
   choco install nssm
   ```

2. Create service:
   ```cmd
   nssm install VideoTranscoder "C:\path\to\venv\Scripts\python.exe" "C:\path\to\app.py"
   ```

3. Configure:
   ```cmd
   nssm set VideoTranscoder AppDirectory "C:\path\to\video-transcoder"
   ```

4. Start service:
   ```cmd
   nssm start VideoTranscoder
   ```

## 📚 Additional Resources

- **Python Docs:** https://docs.python.org/3/
- **FFmpeg Docs:** https://ffmpeg.org/documentation.html
- **Flask Docs:** https://flask.palletsprojects.com/

## 🆘 Getting Help

If you encounter issues:

1. Check the error message carefully
2. Verify Python and FFmpeg are installed correctly
3. Make sure all paths use Windows format
4. Try running as Administrator
5. Check Windows Event Viewer for detailed errors

## ✅ Verification Checklist

- [ ] Python installed and in PATH
- [ ] FFmpeg installed and in PATH
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Directories created (videos/source, videos/output)
- [ ] App starts without errors
- [ ] Web interface accessible at http://localhost:5000
- [ ] Can configure source/output folders
- [ ] Can scan for videos

---

**Everything working? Great! Start transcoding! 🎬✨**