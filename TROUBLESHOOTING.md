# 🔧 Troubleshooting: "was unexpected at this time" Error

## What This Error Means

The error `: was unexpected at this time` is a Windows batch file syntax error. It typically happens when:

1. Special characters in paths or output confuse the batch parser
2. Variables aren't being expanded correctly
3. Conditional statements have syntax issues
4. Command output contains unexpected characters

## ✅ Fixed!

We've fixed the `start.bat` and `install.bat` files to handle this error. The fixes include:

1. **Added `setlocal enabledelayedexpansion`** - Proper variable handling
2. **Changed `%errorlevel%` to `!errorlevel!`** - Delayed variable expansion
3. **Removed problematic FFmpeg output parsing** - Used simpler `where ffmpeg` command
4. **Better error handling** - More robust conditional checks

## 🚀 Try Again

Now run:

```cmd
start.bat
```

It should work without the error!

## 🐛 If You Still Get Errors

### Error: "Python is not installed"

**Solution:**
```cmd
python --version
```

If this fails:
1. Install Python from https://www.python.org/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Restart Command Prompt
4. Try again

### Error: "FFmpeg is not installed"

**Solution:**
Choose one method:

**Option 1 - Chocolatey (Easiest):**
```cmd
choco install ffmpeg
```

**Option 2 - Scoop:**
```cmd
scoop install ffmpeg
```

**Option 3 - winget:**
```cmd
winget install Gyan.FFmpeg
```

**Option 4 - Manual:**
1. Download from https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH
4. Restart Command Prompt

Verify:
```cmd
ffmpeg -version
```

### Error: "Failed to create virtual environment"

**Solution:**
```cmd
REM Delete existing venv if corrupted
rmdir /s /q venv

REM Try again
python -m venv venv
```

### Error: "Failed to install dependencies"

**Solution:**
```cmd
REM Activate virtual environment first
venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt
```

### Error: "venv\Scripts\activate.bat not found"

**Solution:**
The virtual environment wasn't created properly.

```cmd
REM Delete and recreate
rmdir /s /q venv
python -m venv venv
```

## 🔍 Debug Mode

If you still have issues, run in debug mode:

Create `start-debug.bat`:
```batch
@echo off
echo on
REM This shows each command as it runs

python --version
pause

python -m venv venv
pause

call venv\Scripts\activate.bat
pause

pip install -r requirements.txt
pause

python app.py
pause
```

This will show you exactly where it fails.

## 📝 Common Causes and Solutions

### 1. Path Contains Special Characters

**Problem:**
```
C:\Users\John's Files\video-transcoder
```

The apostrophe (`'`) can cause issues.

**Solution:**
Move to a path without special characters:
```
C:\Users\John\video-transcoder
```

### 2. Long Path Names

**Problem:**
```
C:\Users\Username\Documents\My Projects\Video Tools\video-transcoder-application\
```

**Solution:**
Shorten the path:
```
C:\video-transcoder
```

Or enable long paths:
```cmd
reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
```
Then restart.

### 3. Antivirus Blocking

**Problem:**
Antivirus blocks `python.exe` or `pip.exe`

**Solution:**
1. Temporarily disable antivirus
2. Run `install.bat`
3. Add exception for the `venv` folder
4. Re-enable antivirus

### 4. Old Command Prompt Session

**Problem:**
You installed Python/FFmpeg but Command Prompt doesn't see it.

**Solution:**
Close ALL Command Prompt windows and open a new one.

### 5. Wrong Python Version

**Problem:**
Python 2.7 or very old Python 3.x

**Solution:**
```cmd
python --version
```

Should show Python 3.8 or higher. If not:
1. Uninstall old Python
2. Install Python 3.11+ from https://www.python.org/
3. Check "Add to PATH"

## 🆘 Still Not Working?

Try the **manual setup**:

```cmd
REM 1. Create virtual environment
python -m venv venv

REM 2. Activate it
venv\Scripts\activate.bat

REM 3. Upgrade pip
python -m pip install --upgrade pip

REM 4. Install dependencies
pip install -r requirements.txt

REM 5. Create folders
mkdir videos\source
mkdir videos\output

REM 6. Copy config
copy .env.example .env

REM 7. Run the app
python app.py
```

## ✅ Verification Checklist

Run these commands to verify everything:

```cmd
REM Check Python
python --version
REM Should show: Python 3.8 or higher

REM Check pip
pip --version
REM Should show pip version

REM Check FFmpeg
ffmpeg -version
REM Should show FFmpeg version

REM Check virtual environment
dir venv\Scripts\activate.bat
REM Should show file found

REM Check requirements file
dir requirements.txt
REM Should show file found
```

All checks pass? Run `start.bat` again!

## 📞 Get More Help

If none of these work:

1. Open an issue on GitHub with:
   - Your Windows version
   - Python version
   - The exact error message
   - Output of `start-debug.bat`

2. Check the logs:
   - Look for `app.log` file
   - Check Windows Event Viewer

---

**The updated `start.bat` should now work correctly! Give it a try! 🚀**
