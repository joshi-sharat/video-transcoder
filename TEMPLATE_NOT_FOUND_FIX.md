# 🔧 FIXED: Template Not Found Error

## ❌ The Error You're Seeing

```
jinja2.exceptions.TemplateNotFound: index.html
```

## 🎯 What This Means

Flask cannot find the `templates/index.html` file. This happens when:

1. ✅ **Most Common:** The ZIP file wasn't extracted completely
2. Files are in the wrong location
3. The `templates` folder is missing or empty
4. You're running the app from the wrong directory

---

## ✅ SOLUTION: Re-Extract the ZIP File Properly

### **Step 1: Delete Your Current Folder**

Delete the incomplete `video-transcoder` folder you have now.

### **Step 2: Extract ZIP Correctly**

**Windows 11/10 Built-in Extractor:**
1. Right-click `video-transcoder.zip`
2. Click "Extract All..."
3. Choose destination folder
4. **IMPORTANT:** Check "Show extracted files when complete"
5. Click "Extract"

**7-Zip (Recommended):**
1. Right-click `video-transcoder.zip`
2. Choose "7-Zip" → "Extract to video-transcoder\"
3. Done!

**WinRAR:**
1. Right-click `video-transcoder.zip`
2. Choose "Extract to video-transcoder\"
3. Done!

### **Step 3: Verify the Structure**

After extraction, your folder should look like this:

```
video-transcoder\
├── app\
│   ├── __init__.py
│   ├── config.py
│   ├── transcoder.py
│   └── watcher.py
├── templates\              ← MUST EXIST!
│   └── index.html          ← MUST EXIST!
├── static\                 ← MUST EXIST!
│   ├── css\
│   │   └── style.css
│   └── js\
│       └── app.js
├── videos\
│   ├── source\
│   └── output\
├── app.py
├── requirements.txt
├── start.bat
├── check-structure.bat     ← Run this to verify!
└── ... (other files)
```

### **Step 4: Run Structure Check**

Open Command Prompt in the `video-transcoder` folder and run:

```cmd
check-structure.bat
```

This will tell you exactly what's missing.

You should see:

```
========================================
  Folder Structure Check
========================================

[OK] templates\ folder exists
[OK] templates\index.html exists
[OK] static\ folder exists
[OK] static\css\ folder exists
[OK] static\css\style.css exists
[OK] static\js\ folder exists
[OK] static\js\app.js exists
[OK] app\ folder exists
[OK] app\__init__.py exists
[OK] app\config.py exists
[OK] app\transcoder.py exists
[OK] app\watcher.py exists
[OK] app.py exists
[OK] requirements.txt exists

========================================
[SUCCESS] All files and folders are in place!
You can now run: start.bat
========================================
```

### **Step 5: Run the Application**

Now run:

```cmd
start.bat
```

It should work!

---

## 🔍 Common Extraction Mistakes

### ❌ Wrong: Extracting Only Some Files

Some users:
- Extract only `.py` files
- Miss the `templates` and `static` folders
- Extract to nested folders

### ❌ Wrong: Nested Extraction

If you see:
```
video-transcoder\
└── video-transcoder\
    ├── app\
    ├── templates\    ← Templates are here but you're running from parent!
    └── app.py
```

You're in the wrong folder! Go one level deeper.

### ❌ Wrong: Running from Wrong Directory

If you run `start.bat` from:
```
C:\Downloads\start.bat
```

But files are in:
```
C:\Downloads\video-transcoder\
```

The app won't find templates. Always run from inside the `video-transcoder` folder!

---

## 🐛 Still Not Working?

### Check 1: Are You in the Right Folder?

```cmd
dir
```

You should see:
- `app` (folder)
- `templates` (folder)
- `static` (folder)
- `app.py` (file)
- `start.bat` (file)

If not, you're in the wrong folder!

### Check 2: Does templates\index.html Exist?

```cmd
dir templates\index.html
```

Should show:
```
 Directory of C:\...\video-transcoder\templates
index.html
```

If you get "File Not Found", the template is missing!

### Check 3: Full Path Check

```cmd
cd
```

Make sure the path doesn't have the project name twice:
```
❌ C:\video-transcoder\video-transcoder\  (Wrong - nested)
✅ C:\video-transcoder\                   (Correct)
```

---

## 💡 Prevention Tips

1. **Use a good ZIP extractor:**
   - Windows built-in (works fine)
   - 7-Zip (best)
   - WinRAR (works)
   - Avoid: Partial extractors

2. **Extract to a simple path:**
   - ✅ `C:\video-transcoder`
   - ✅ `C:\Projects\video-transcoder`
   - ❌ `C:\Users\John's Files\Downloads\New Folder (2)\video-transcoder`

3. **Extract ALL files:**
   - Don't skip folders
   - Don't extract only Python files
   - Extract the complete structure

4. **Verify before running:**
   - Run `check-structure.bat` first
   - Confirms everything is in place

---

## 📝 Quick Fix Checklist

- [ ] Delete incomplete extraction
- [ ] Re-extract video-transcoder.zip completely
- [ ] Run `check-structure.bat`
- [ ] All checks pass?
- [ ] Run `start.bat`
- [ ] Open http://localhost:5000
- [ ] Works! 🎉

---

## 🆘 Emergency Manual Setup

If ZIP extraction keeps failing, download files individually:

1. Create folder structure manually:
```cmd
mkdir video-transcoder
cd video-transcoder
mkdir app
mkdir templates
mkdir static\css
mkdir static\js
mkdir videos\source
mkdir videos\output
```

2. Download individual files and place them correctly

3. Run `check-structure.bat` to verify

---

## ✅ Fixed start.bat

The new `start.bat` now checks for templates **before** starting:

```batch
REM Check folder structure first
if not exist "templates\index.html" (
    echo [ERROR] templates\index.html not found!
    echo Please re-extract the ZIP file completely.
    pause
    exit /b 1
)
```

This prevents the Flask error and gives you a clear message!

---

**Download the updated ZIP and extract it properly - the issue will be resolved!** 🚀
