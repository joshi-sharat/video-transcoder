import os
import json
import threading
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import psutil
from app.transcoder import VideoTranscoder
from app.watcher import FolderWatcher
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = SQLAlchemy(app)

# Global instances
transcoder = None
watcher = None

# Database Models
class TranscodeJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_file = db.Column(db.String(500), nullable=False)
    output_file = db.Column(db.String(500))
    status = db.Column(db.String(50), default='pending')
    progress = db.Column(db.Float, default=0.0)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'source_file': self.source_file,
            'output_file': self.output_file,
            'status': self.status,
            'progress': self.progress,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    
    @staticmethod
    def get_value(key, default=None):
        setting = Settings.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set_value(key, value):
        setting = Settings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = Settings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()

# Initialize database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get current settings"""
    return jsonify({
        'source_folder': Settings.get_value('source_folder', ''),
        'output_folder': Settings.get_value('output_folder', ''),
        'watch_enabled': Settings.get_value('watch_enabled', 'false') == 'true',
        'output_format': Settings.get_value('output_format', 'mp4'),
        'video_codec': Settings.get_value('video_codec', 'libx264'),
        'audio_codec': Settings.get_value('audio_codec', 'aac'),
        'preset': Settings.get_value('preset', 'medium'),
        'crf': Settings.get_value('crf', '23')
    })

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update settings"""
    global watcher
    
    data = request.json
    
    # Validate folders
    source_folder = data.get('source_folder', '')
    output_folder = data.get('output_folder', '')
    
    if source_folder and not os.path.exists(source_folder):
        return jsonify({'error': 'Source folder does not exist'}), 400
    
    if output_folder and not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder, exist_ok=True)
        except Exception as e:
            return jsonify({'error': f'Cannot create output folder: {str(e)}'}), 400
    
    # Save settings
    Settings.set_value('source_folder', source_folder)
    Settings.set_value('output_folder', output_folder)
    Settings.set_value('watch_enabled', 'true' if data.get('watch_enabled') else 'false')
    Settings.set_value('output_format', data.get('output_format', 'mp4'))
    Settings.set_value('video_codec', data.get('video_codec', 'libx264'))
    Settings.set_value('audio_codec', data.get('audio_codec', 'aac'))
    Settings.set_value('preset', data.get('preset', 'medium'))
    Settings.set_value('crf', str(data.get('crf', 23)))
    
    # Restart watcher if enabled
    if data.get('watch_enabled') and source_folder:
        if watcher:
            watcher.stop()
        watcher = FolderWatcher(source_folder, on_new_file)
        watcher.start()
    elif watcher:
        watcher.stop()
        watcher = None
    
    return jsonify({'message': 'Settings updated successfully'})

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all transcode jobs"""
    status = request.args.get('status')
    query = TranscodeJob.query
    
    if status:
        query = query.filter_by(status=status)
    
    jobs = query.order_by(TranscodeJob.created_at.desc()).all()
    return jsonify([job.to_dict() for job in jobs])

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get specific job details"""
    job = TranscodeJob.query.get_or_404(job_id)
    return jsonify(job.to_dict())

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new transcode job"""
    data = request.json
    source_file = data.get('source_file')
    
    if not source_file or not os.path.exists(source_file):
        return jsonify({'error': 'Source file does not exist'}), 400
    
    job = TranscodeJob(source_file=source_file, status='pending')
    db.session.add(job)
    db.session.commit()
    
    # Start transcoding in background
    threading.Thread(target=process_job, args=(job.id,), daemon=True).start()
    
    return jsonify(job.to_dict()), 201

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job"""
    job = TranscodeJob.query.get_or_404(job_id)
    
    if job.status == 'processing':
        return jsonify({'error': 'Cannot delete job in progress'}), 400
    
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({'message': 'Job deleted successfully'})

@app.route('/api/scan', methods=['POST'])
def scan_folder():
    """Scan source folder for new videos"""
    source_folder = Settings.get_value('source_folder')
    
    if not source_folder or not os.path.exists(source_folder):
        return jsonify({'error': 'Source folder not configured or does not exist'}), 400
    
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.m4v', '.webm'}
    new_files = []
    
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if Path(file).suffix.lower() in video_extensions:
                file_path = os.path.join(root, file)
                # Check if already in database
                existing = TranscodeJob.query.filter_by(source_file=file_path).first()
                if not existing:
                    new_files.append(file_path)
    
    # Create jobs for new files
    jobs_created = []
    for file_path in new_files:
        job = TranscodeJob(source_file=file_path, status='pending')
        db.session.add(job)
        jobs_created.append(job)
    
    db.session.commit()
    
    # Start processing
    for job in jobs_created:
        threading.Thread(target=process_job, args=(job.id,), daemon=True).start()
    
    return jsonify({
        'message': f'Found {len(new_files)} new files',
        'jobs': [job.to_dict() for job in jobs_created]
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    total_jobs = TranscodeJob.query.count()
    pending_jobs = TranscodeJob.query.filter_by(status='pending').count()
    processing_jobs = TranscodeJob.query.filter_by(status='processing').count()
    completed_jobs = TranscodeJob.query.filter_by(status='completed').count()
    failed_jobs = TranscodeJob.query.filter_by(status='failed').count()
    
    return jsonify({
        'total_jobs': total_jobs,
        'pending_jobs': pending_jobs,
        'processing_jobs': processing_jobs,
        'completed_jobs': completed_jobs,
        'failed_jobs': failed_jobs,
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'watch_enabled': Settings.get_value('watch_enabled', 'false') == 'true'
    })

# Background processing
def process_job(job_id):
    """Process a transcode job"""
    with app.app_context():
        job = TranscodeJob.query.get(job_id)
        if not job:
            return
        
        job.status = 'processing'
        job.started_at = datetime.utcnow()
        db.session.commit()
        
        try:
            output_folder = Settings.get_value('output_folder')
            output_format = Settings.get_value('output_format', 'mp4')
            
            # Generate output filename
            source_path = Path(job.source_file)
            output_filename = f"{source_path.stem}_transcoded.{output_format}"
            output_path = os.path.join(output_folder, output_filename)
            
            # Get transcoding settings
            settings = {
                'video_codec': Settings.get_value('video_codec', 'libx264'),
                'audio_codec': Settings.get_value('audio_codec', 'aac'),
                'preset': Settings.get_value('preset', 'medium'),
                'crf': int(Settings.get_value('crf', '23'))
            }
            
            # Transcode
            transcoder = VideoTranscoder()
            
            def progress_callback(progress):
                job.progress = progress
                db.session.commit()
            
            transcoder.transcode(
                job.source_file,
                output_path,
                settings,
                progress_callback
            )
            
            job.output_file = output_path
            job.status = 'completed'
            job.progress = 100.0
            job.completed_at = datetime.utcnow()
            
        except Exception as e:
            job.status = 'failed'
            job.error_message = str(e)
        
        db.session.commit()

def on_new_file(file_path):
    """Callback when new file is detected"""
    with app.app_context():
        # Check if file already exists in database
        existing = TranscodeJob.query.filter_by(source_file=file_path).first()
        if not existing:
            job = TranscodeJob(source_file=file_path, status='pending')
            db.session.add(job)
            db.session.commit()
            
            # Start processing
            threading.Thread(target=process_job, args=(job.id,), daemon=True).start()


if __name__ == '__main__':
    print("Starting Video Transcoder...")

    # Wrapped in app context - WORKS!
    with app.app_context():
        try:
            watch_enabled = Settings.get_value('watch_enabled', 'false')
            ...
        except Exception as e:
            print(f"Warning: {e}")

    app.run(host='0.0.0.0', port=5000, debug=True)
