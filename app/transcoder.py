import os
import subprocess
import re
import ffmpeg
from pathlib import Path


class VideoTranscoder:
    """Handle video transcoding operations"""

    def __init__(self):
        self.ffmpeg_path = 'ffmpeg'
        self.ffprobe_path = 'ffprobe'

    def get_video_duration(self, input_file):
        """Get video duration in seconds"""
        try:
            probe = ffmpeg.probe(input_file)
            duration = float(probe['format']['duration'])
            return duration
        except Exception as e:
            print(f"Error getting video duration: {e}")
            return 0

    def transcode(self, input_file, output_file, settings, progress_callback=None):
        """
        Transcode a video file

        Args:
            input_file: Path to input video file
            output_file: Path to output video file
            settings: Dictionary with transcoding settings
            progress_callback: Optional callback function for progress updates
        """
        video_codec = settings.get('video_codec', 'libx264')
        audio_codec = settings.get('audio_codec', 'aac')
        preset = settings.get('preset', 'medium')
        crf = settings.get('crf', 23)

        # Build FFmpeg command
        cmd = [
            self.ffmpeg_path,
            '-i', input_file,
            '-c:v', video_codec,
            '-preset', preset,
            '-crf', str(crf),
            '-c:a', audio_codec,
            '-b:a', '192k',
            '-movflags', '+faststart',
            '-y',  # Overwrite output file
            '-progress', 'pipe:1',  # Output progress to stdout
            output_file
        ]

        # Get total duration for progress calculation
        total_duration = self.get_video_duration(input_file)

        # Run FFmpeg
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        # Parse progress
        for line in process.stdout:
            if progress_callback and total_duration > 0:
                # Look for time progress
                time_match = re.search(r'out_time_ms=(\d+)', line)
                if time_match:
                    current_time = int(time_match.group(1)) / 1000000  # Convert microseconds to seconds
                    progress = min(100.0, (current_time / total_duration) * 100)
                    progress_callback(progress)

        process.wait()

        if process.returncode != 0:
            raise Exception(f"FFmpeg failed with return code {process.returncode}")

        if progress_callback:
            progress_callback(100.0)

        return output_file

    def get_video_info(self, input_file):
        """Get detailed information about a video file"""
        try:
            probe = ffmpeg.probe(input_file)

            video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
            audio_stream = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)

            info = {
                'duration': float(probe['format']['duration']),
                'size': int(probe['format']['size']),
                'bitrate': int(probe['format']['bit_rate']),
                'format': probe['format']['format_name']
            }

            if video_stream:
                info['video'] = {
                    'codec': video_stream['codec_name'],
                    'width': video_stream['width'],
                    'height': video_stream['height'],
                    'fps': eval(video_stream.get('r_frame_rate', '0/1'))
                }

            if audio_stream:
                info['audio'] = {
                    'codec': audio_stream['codec_name'],
                    'sample_rate': int(audio_stream.get('sample_rate', 0)),
                    'channels': audio_stream.get('channels', 0)
                }

            return info

        except Exception as e:
            print(f"Error getting video info: {e}")
            return None