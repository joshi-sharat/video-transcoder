# 📂 Manual Setup Instructions

If you downloaded individual files instead of the ZIP, here's how to set up the folder structure:

## Step 1: Create the Folder Structure

```bash
mkdir -p video-transcoder/app
mkdir -p video-transcoder/static/css
mkdir -p video-transcoder/static/js
mkdir -p video-transcoder/templates
mkdir -p video-transcoder/videos/source
mkdir -p video-transcoder/videos/output
cd video-transcoder
```

## Step 2: Place Files in Their Correct Locations

### Root Directory Files:
```
video-transcoder/
├── app.py                    ← Main Flask application
├── requirements.txt          ← Python dependencies
├── start.sh                  ← Startup script
├── test_api.sh              ← API testing script
├── push_to_github.sh        ← GitHub push helper
├── Dockerfile               ← Docker configuration
├── docker-compose.yml       ← Docker Compose config
├── .env.example             ← Environment template
├── .gitignore               ← Git ignore rules
├── README.md                ← Full documentation
├── QUICKSTART.md            ← Quick start guide
├── GITHUB_SETUP.md          ← GitHub setup guide
└── video-transcoder.service ← Systemd service
```

### App Folder (app/):
**IMPORTANT**: Create an `app` folder and put these 4 files inside it:
```
app/
├── __init__.py      ← Package initialization (can be empty or minimal)
├── config.py        ← Application configuration
├── transcoder.py    ← Video transcoding engine
└── watcher.py       ← Folder monitoring logic
```

### Static Folder (static/):
```
static/
├── css/
│   └── style.css    ← Stylesheet
└── js/
    └── app.js       ← Frontend JavaScript
```

### Templates Folder (templates/):
```
templates/
└── index.html       ← Web interface HTML
```

### Videos Folder (videos/):
```
videos/
├── source/          ← Source videos go here (can be empty)
└── output/          ← Transcoded videos saved here (can be empty)
```

## Step 3: Make Scripts Executable

```bash
chmod +x start.sh test_api.sh push_to_github.sh
```

## Step 4: Verify Structure

Run this to verify your structure is correct:

```bash
ls -R
```

You should see:
```
.:
app  app.py  Dockerfile  docker-compose.yml  README.md  requirements.txt  start.sh  static  templates  videos

./app:
__init__.py  config.py  transcoder.py  watcher.py

./static:
css  js

./static/css:
style.css

./static/js:
app.js

./templates:
index.html

./videos:
output  source
```

## Step 5: Install and Run

```bash
./start.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 🎯 EASIER OPTION: Download the ZIP

Instead of manually placing files, download the **video-transcoder.zip** file which contains the complete folder structure. Just extract it and you're done!

```bash
unzip video-transcoder.zip
cd video-transcoder
./start.sh
```

## ✅ Checklist

Make sure you have:
- ✅ Created the `app/` folder
- ✅ Placed all 4 files in `app/` folder:
  - `__init__.py`
  - `config.py`
  - `transcoder.py`
  - `watcher.py`
- ✅ Created `static/css/` and `static/js/` folders
- ✅ Placed `style.css` in `static/css/`
- ✅ Placed `app.js` in `static/js/`
- ✅ Created `templates/` folder
- ✅ Placed `index.html` in `templates/`
- ✅ All other files in root directory

If you're missing the folder structure, the app will fail with import errors!
