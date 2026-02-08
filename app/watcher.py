import time
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class VideoFileHandler(FileSystemEventHandler):
    """Handle filesystem events for video files"""

    def __init__(self, callback, video_extensions=None):
        self.callback = callback
        self.video_extensions = video_extensions or {
            '.mp4', '.avi', '.mkv', '.mov', '.flv',
            '.wmv', '.m4v', '.webm', '.mpg', '.mpeg'
        }
        self.processing_files = set()

    def on_created(self, event):
        """Called when a file is created"""
        if event.is_directory:
            return

        file_path = event.src_path
        file_ext = Path(file_path).suffix.lower()

        # Check if it's a video file
        if file_ext in self.video_extensions:
            # Wait for file to be completely written
            time.sleep(2)

            # Check if file is complete and not being processed
            if os.path.exists(file_path) and file_path not in self.processing_files:
                self.processing_files.add(file_path)
                try:
                    self.callback(file_path)
                finally:
                    # Remove from processing set after a delay
                    time.sleep(1)
                    self.processing_files.discard(file_path)


class FolderWatcher:
    """Watch a folder for new video files"""

    def __init__(self, folder_path, callback):
        self.folder_path = folder_path
        self.callback = callback
        self.observer = None
        self.handler = None

    def start(self):
        """Start watching the folder"""
        if not os.path.exists(self.folder_path):
            raise ValueError(f"Folder does not exist: {self.folder_path}")

        self.handler = VideoFileHandler(self.callback)
        self.observer = Observer()
        self.observer.schedule(self.handler, self.folder_path, recursive=True)
        self.observer.start()
        print(f"Started watching folder: {self.folder_path}")

    def stop(self):
        """Stop watching the folder"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print(f"Stopped watching folder: {self.folder_path}")

    def is_running(self):
        """Check if watcher is running"""
        return self.observer and self.observer.is_alive()