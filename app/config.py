import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""

    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///transcoder.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 * 1024  # 16GB max file size

    # FFmpeg settings
    FFMPEG_PATH = os.getenv('FFMPEG_PATH', 'ffmpeg')
    FFPROBE_PATH = os.getenv('FFPROBE_PATH', 'ffprobe')

    # Supported video formats
    SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.m4v', '.webm', '.mpg', '.mpeg']

    # Default transcoding settings
    DEFAULT_VIDEO_CODEC = 'libx264'
    DEFAULT_AUDIO_CODEC = 'aac'
    DEFAULT_PRESET = 'medium'
    DEFAULT_CRF = 23
    DEFAULT_OUTPUT_FORMAT = 'mp4'