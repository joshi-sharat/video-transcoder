# 🔧 FIXED: Flask Application Context Error

## ❌ The Error You Had

```
RuntimeError: Working outside of application context.
This typically means that you attempted to use functionality that needed
the current application. To solve this, set up an application context
with app.app_context().
```

## ✅ What Was Wrong

The `app.py` file was trying to access the database (`Settings.get_value()`) **before** Flask had set up the application context. This happens when:

1. Database queries run outside `app.app_context()`
2. Code tries to use `db` objects before Flask is ready
3. Startup code accesses models before the app starts

## 🔨 What I Fixed

### **In app.py:**

**BEFORE (Broken):**
```python
if __name__ == '__main__':
    # This runs OUTSIDE app context - ERROR!
    if Settings.get_value('watch_enabled', 'false') == 'true':
        source_folder = Settings.get_value('source_folder')
        ...
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**AFTER (Fixed):**
```python
if __name__ == '__main__':
    print("Starting Video Transcoder...")
    
    # Wrapped in app context - WORKS!
    with app.app_context():
        try:
            watch_enabled = Settings.get_value('watch_enabled', 'false')
            if watch_enabled == 'true':
                source_folder = Settings.get_value('source_folder')
                ...
        except Exception as e:
            print(f"Warning: Could not initialize folder watcher: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## 🎯 Key Changes

1. ✅ **Wrapped database access in `with app.app_context():`**
2. ✅ **Added try/except for better error handling**
3. ✅ **Added helpful print statements**
4. ✅ **Made it fail gracefully if watcher can't start**

## 🚀 Try It Now!

Download the updated files and run:

```cmd
start.bat
```

You should now see:

```
Starting Video Transcoder...
Initializing database...
Starting Flask server...
Web interface available at: http://localhost:5000
Press Ctrl+C to stop
--------------------------------------------------
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
```

## 📚 Understanding Flask Application Context

### What is Application Context?

Flask uses "contexts" to make certain objects available during request handling. The **application context** makes `current_app` and `g` available, and more importantly, it sets up database connections.

### When Do You Need It?

**You DON'T need app context:**
```python
# Inside route handlers - Flask provides context automatically
@app.route('/api/jobs')
def get_jobs():
    jobs = TranscodeJob.query.all()  # Works fine!
    return jsonify([job.to_dict() for job in jobs])
```

**You DO need app context:**
```python
# Outside route handlers - Must create context manually
if __name__ == '__main__':
    with app.app_context():
        jobs = TranscodeJob.query.all()  # Now it works!
```

### Common Scenarios Needing App Context

1. **Startup code** (like our watcher initialization)
2. **CLI commands** or management scripts
3. **Background tasks** outside request handlers
4. **Testing** database operations

## 🐛 Other Common Flask Errors

### Error: "RuntimeError: No application found"

**Cause:** Trying to use Flask extensions before app is created

**Fix:**
```python
# WRONG
db = SQLAlchemy()
app = Flask(__name__)

# RIGHT
app = Flask(__name__)
db = SQLAlchemy(app)
```

### Error: "sqlite3.OperationalError: no such table"

**Cause:** Database tables not created

**Fix:**
```python
with app.app_context():
    db.create_all()
```

This is already in the fixed `app.py`!

### Error: "RuntimeError: Working outside of request context"

**Cause:** Trying to access `request` object outside a route

**Fix:** Only access `request` inside route handlers or use `with app.test_request_context()`

## ✅ Verification

After starting the app, you should be able to:

1. **Access the web interface:** http://localhost:5000
2. **See the dashboard** with settings and jobs sections
3. **Configure folders** without errors
4. **Scan for videos** without errors

## 📝 What Got Fixed

| File | What Changed |
|------|-------------|
| `app.py` | Added `with app.app_context():` around startup code |
| `app.py` | Added error handling for watcher initialization |
| `app.py` | Added helpful console messages |
| `start.bat` | Simplified to avoid batch syntax errors |

## 🎉 You're All Set!

The application context error is now fixed. Download the updated ZIP and run `start.bat` - it should work perfectly now!

---

**Still having issues?** Check:
1. Python version (should be 3.8+): `python --version`
2. All dependencies installed: `pip list`
3. Database file created: Check for `transcoder.db` or `instance/transcoder.db`
4. No other app using port 5000: `netstat -ano | findstr :5000`
