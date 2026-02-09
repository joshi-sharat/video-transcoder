# 🐛 Debugging Guide - Video Transcoder

## Quick Start: Run in Debug Mode

### Option 1: Flask Debug Mode (Simplest)

The app is already configured for debug mode. Just run:

```bash
python app.py
```

Debug mode is enabled by default in `app/config.py`:
```python
DEBUG = os.getenv('DEBUG', 'True') == 'True'
```

**Features enabled in debug mode:**
- ✅ Auto-reload on code changes
- ✅ Detailed error pages with stack traces
- ✅ Interactive debugger in browser

---

## Debugging with Breakpoints

### Option 2: Python pdb (Built-in Debugger)

Add breakpoints in your code where you want to pause execution:

#### Example: Debug an API endpoint

Edit `app.py` and add `import pdb; pdb.set_trace()` where you want to stop:

```python
@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update settings"""
    import pdb; pdb.set_trace()  # ← BREAKPOINT HERE
    
    data = request.json
    # ... rest of the code
```

Then run:
```bash
python app.py
```

When you hit the API endpoint (e.g., POST to `/api/settings`), the server will pause and drop into the debugger:

```
> /app/app.py(123)update_settings()
-> data = request.json
(Pdb) 
```

**Common pdb commands:**
```
n (next)       - Execute next line
s (step)       - Step into function
c (continue)   - Continue execution
p variable     - Print variable value
l (list)       - Show current code
h (help)       - Show help
q (quit)       - Exit debugger
```

---

### Option 3: Using breakpoint() (Python 3.7+)

Python 3.7+ has a built-in `breakpoint()` function:

```python
@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new transcode job"""
    data = request.json
    source_file = data.get('source_file')
    
    breakpoint()  # ← STOPS HERE
    
    if not source_file or not os.path.exists(source_file):
        return jsonify({'error': 'Source file does not exist'}), 400
```

---

### Option 4: VS Code Debugging (Recommended for IDEs)

#### Step 1: Create `.vscode/launch.json`

Create this file in your project root:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload",
                "--host=0.0.0.0",
                "--port=5000"
            ],
            "jinja": true,
            "justMyCode": true,
            "console": "integratedTerminal"
        }
    ]
}
```

#### Step 2: Set Breakpoints

1. Open `app.py` in VS Code
2. Click left of line number to set red dot breakpoint
3. Press F5 to start debugging
4. Make API call - execution will pause at breakpoint

**VS Code Debug Controls:**
- F5 - Continue
- F10 - Step Over
- F11 - Step Into
- Shift+F11 - Step Out
- Ctrl+Shift+F5 - Restart
- Shift+F5 - Stop

---

### Option 5: PyCharm Debugging

1. Open project in PyCharm
2. Right-click `app.py` → "Debug 'app'"
3. Click left gutter to set breakpoints
4. Run debugger
5. Make API calls to trigger breakpoints

---

## Debugging Specific Scenarios

### 1. Debug API Endpoint

Add breakpoint in the endpoint you want to debug:

```python
@app.route('/api/scan', methods=['POST'])
def scan_folder():
    import pdb; pdb.set_trace()  # ← STOPS HERE
    
    source_folder = Settings.get_value('source_folder')
    # ... rest of code
```

Test with curl:
```bash
curl -X POST http://localhost:5000/api/scan
```

### 2. Debug Transcoding Logic

Add breakpoint in `app/transcoder.py`:

```python
def transcode(self, input_file, output_file, settings, progress_callback=None):
    import pdb; pdb.set_trace()  # ← STOPS HERE
    
    video_codec = settings.get('video_codec', 'libx264')
    # ... rest of code
```

### 3. Debug Folder Watcher

Add breakpoint in `app/watcher.py`:

```python
def on_created(self, event):
    """Called when a file is created"""
    import pdb; pdb.set_trace()  # ← STOPS HERE
    
    if event.is_directory:
        return
    # ... rest of code
```

### 4. Debug Database Operations

```python
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    import pdb; pdb.set_trace()  # ← STOPS HERE
    
    status = request.args.get('status')
    query = TranscodeJob.query
    # ... rest of code
```

---

## Advanced Debugging

### Remote Debugging (debugpy)

For debugging in production or containers:

```bash
pip install debugpy
```

Add to `app.py` before `if __name__ == '__main__'`:

```python
import debugpy

# Allow VS Code to attach to the running process
debugpy.listen(("0.0.0.0", 5678))
print("⏳ Waiting for debugger to attach...")
debugpy.wait_for_client()
print("✅ Debugger attached!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

VS Code attach configuration:
```json
{
    "name": "Python: Attach",
    "type": "python",
    "request": "attach",
    "connect": {
        "host": "localhost",
        "port": 5678
    }
}
```

---

## Logging for Debugging

### Add Detailed Logging

Edit `app.py` to add logging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in endpoints
@app.route('/api/settings', methods=['POST'])
def update_settings():
    logger.debug(f"Received settings update request")
    data = request.json
    logger.debug(f"Settings data: {data}")
    # ... rest of code
```

View logs:
```bash
tail -f app.log
```

---

## Debugging Tips

### 1. Inspect Request Data

```python
@app.route('/api/jobs', methods=['POST'])
def create_job():
    print("=" * 50)
    print("REQUEST DEBUG INFO")
    print("=" * 50)
    print(f"Method: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Data: {request.get_data()}")
    print(f"JSON: {request.json}")
    print("=" * 50)
    
    # Your code here
```

### 2. Inspect Database State

```python
# Check what's in the database
@app.route('/api/debug/jobs')
def debug_jobs():
    jobs = TranscodeJob.query.all()
    return jsonify([{
        'id': j.id,
        'source': j.source_file,
        'status': j.status,
        'progress': j.progress
    } for j in jobs])
```

### 3. Test Individual Functions

Create a test script `test_debug.py`:

```python
from app.transcoder import VideoTranscoder
from app.config import Config

# Test transcoder directly
transcoder = VideoTranscoder()
info = transcoder.get_video_info('/path/to/test.mp4')
print(info)
```

Run:
```bash
python test_debug.py
```

---

## Stop Execution on Specific Conditions

### Conditional Breakpoints

```python
@app.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.json
    source_file = data.get('source_file')
    
    # Only break for specific files
    if 'test' in source_file:
        import pdb; pdb.set_trace()
    
    # Continue normally
```

### Exception Breakpoints

```python
import sys

def excepthook(type, value, traceback):
    import pdb
    pdb.post_mortem(traceback)

sys.excepthook = excepthook
```

Now any unhandled exception will drop into debugger.

---

## Quick Reference

### Start App in Debug Mode
```bash
python app.py                    # Debug enabled by default
FLASK_DEBUG=1 python app.py     # Explicitly enable debug
```

### Add Breakpoint
```python
import pdb; pdb.set_trace()     # Python 2.7+
breakpoint()                     # Python 3.7+
```

### Test API Endpoints
```bash
# GET request
curl http://localhost:5000/api/status

# POST request
curl -X POST http://localhost:5000/api/settings \
  -H "Content-Type: application/json" \
  -d '{"source_folder": "/tmp/videos"}'

# With debugger, execution will pause at breakpoint
```

### View Logs
```bash
# Real-time logs
tail -f app.log

# Last 50 lines
tail -n 50 app.log
```

---

## Troubleshooting

**Breakpoint not hit?**
- Make sure you're calling the right endpoint
- Check if code path actually reaches the breakpoint
- Verify file is saved before running

**Can't attach debugger?**
- Check firewall settings
- Verify port 5678 (or debug port) is open
- Ensure debugpy is installed

**App won't start in debug mode?**
- Check syntax errors
- Verify all imports work
- Check `.env` file settings

---

## Example: Full Debug Session

1. Add breakpoint to `app.py`:
```python
@app.route('/api/scan', methods=['POST'])
def scan_folder():
    breakpoint()  # STOP HERE
    source_folder = Settings.get_value('source_folder')
```

2. Start app:
```bash
python app.py
```

3. In another terminal, trigger endpoint:
```bash
curl -X POST http://localhost:5000/api/scan
```

4. Debugger activates:
```
> /app.py(189)scan_folder()
-> source_folder = Settings.get_value('source_folder')
(Pdb) p source_folder
*** NameError: name 'source_folder' is not defined
(Pdb) n
> /app.py(191)scan_folder()
-> if not source_folder or not os.path.exists(source_folder):
(Pdb) p source_folder
'/path/to/videos'
(Pdb) c
```

Happy debugging! 🐛✨
