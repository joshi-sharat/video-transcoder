#!/usr/bin/env python3
"""
Debug Example Script - Video Transcoder

This script demonstrates where to add breakpoints for debugging different parts of the application.

Usage:
    1. Uncomment the breakpoint() lines where you want to debug
    2. Run: python app.py
    3. Make API calls to trigger breakpoints
    4. Use debugger commands: n (next), s (step), c (continue), p (print), q (quit)
"""

# Example 1: Debug API Settings Endpoint
def debug_settings_endpoint():
    """
    To debug the settings endpoint:
    1. Add breakpoint in app.py at the update_settings() function
    2. Make a POST request to /api/settings
    """
    example = """
    @app.route('/api/settings', methods=['POST'])
    def update_settings():
        breakpoint()  # ← ADD THIS LINE
        data = request.json
        # ... rest of code
    """
    print(example)

# Example 2: Debug Transcoding Process
def debug_transcoding():
    """
    To debug the transcoding logic:
    1. Add breakpoint in app/transcoder.py
    2. Create a transcode job
    """
    example = """
    # In app/transcoder.py
    def transcode(self, input_file, output_file, settings, progress_callback=None):
        breakpoint()  # ← ADD THIS LINE
        video_codec = settings.get('video_codec', 'libx264')
        # ... rest of code
    """
    print(example)

# Example 3: Debug File Watcher
def debug_watcher():
    """
    To debug the folder watcher:
    1. Add breakpoint in app/watcher.py
    2. Add a video file to the watched folder
    """
    example = """
    # In app/watcher.py
    def on_created(self, event):
        breakpoint()  # ← ADD THIS LINE
        if event.is_directory:
            return
        # ... rest of code
    """
    print(example)

# Example 4: Conditional Breakpoint
def debug_conditional():
    """
    Break only for specific conditions
    """
    example = """
    @app.route('/api/jobs', methods=['POST'])
    def create_job():
        data = request.json
        source_file = data.get('source_file')
        
        # Only debug if source file contains 'test'
        if 'test' in source_file.lower():
            breakpoint()  # ← CONDITIONAL BREAKPOINT
        
        # ... rest of code
    """
    print(example)

# Example 5: Test Individual Components
def test_transcoder():
    """
    Test the transcoder directly without running the full app
    """
    from app.transcoder import VideoTranscoder
    
    transcoder = VideoTranscoder()
    
    # Test getting video info
    # breakpoint()  # Uncomment to debug
    # info = transcoder.get_video_info('/path/to/test.mp4')
    # print(info)
    
    print("Uncomment the breakpoint() line to debug transcoder directly")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Video Transcoder - Debug Examples")
    print("="*60 + "\n")
    
    print("1. Debug Settings Endpoint:")
    debug_settings_endpoint()
    
    print("\n2. Debug Transcoding:")
    debug_transcoding()
    
    print("\n3. Debug File Watcher:")
    debug_watcher()
    
    print("\n4. Conditional Breakpoint:")
    debug_conditional()
    
    print("\n5. Test Individual Components:")
    print("   Run: python debug_examples.py")
    
    print("\n" + "="*60)
    print("Quick Debugger Commands:")
    print("="*60)
    print("  n (next)      - Execute next line")
    print("  s (step)      - Step into function")
    print("  c (continue)  - Continue execution")
    print("  p <var>       - Print variable value")
    print("  l (list)      - Show current code")
    print("  q (quit)      - Exit debugger")
    print("="*60 + "\n")
