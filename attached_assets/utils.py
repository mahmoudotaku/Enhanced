
import os
import time
import uuid
import yt_dlp
from datetime import datetime
from app import app

def generate_download_id():
    """Generate unique download ID"""
    return str(uuid.uuid4()).replace('-', '')[:12]

def format_file_size(bytes_size):
    """Format file size in human readable format"""
    if not bytes_size:
        return "غير محدد"

    for unit in ['بايت', 'كيلوبايت', 'ميجابايت', 'جيجابايت']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} تيرابايت"

def format_duration(seconds):
    """Format duration in human readable format"""
    if not seconds:
        return "غير محدد"

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def get_platform_name(url):
    """Get platform name from URL"""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'YouTube'
    elif 'tiktok.com' in url:
        return 'TikTok'
    elif 'instagram.com' in url:
        return 'Instagram'
    elif 'twitter.com' in url or 'x.com' in url:
        return 'Twitter'
    elif 'facebook.com' in url:
        return 'Facebook'
    elif 'vimeo.com' in url:
        return 'Vimeo'
    else:
        return 'أخرى'

def get_video_info(url):
    """Get video information using yt-dlp"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            'success': True,
            'data': info
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'خطأ في الحصول على معلومات الفيديو: {str(e)}'
        }

def download_video(url, quality='best', download_id=None, progress_callback=None):
    """Download video using yt-dlp"""
    try:
        downloads_dir = app.config['UPLOAD_FOLDER']
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)

        # Set up download options
        ydl_opts = {
            'outtmpl': f'{downloads_dir}/{download_id}_%(title)s.%(ext)s',
            'format': quality if quality != 'mp3' else 'bestaudio/best',
            'postprocessors': [],
        }

        # Add audio conversion for MP3
        if quality == 'mp3':
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })

        # Progress hook
        def progress_hook(d):
            if progress_callback and d['status'] == 'downloading':
                if 'total_bytes' in d and d['total_bytes']:
                    percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    progress_callback(percent)

        ydl_opts['progress_hooks'] = [progress_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the downloaded file
        for file in os.listdir(downloads_dir):
            if file.startswith(f"{download_id}_"):
                filepath = os.path.join(downloads_dir, file)
                file_size = os.path.getsize(filepath)
                return {
                    'success': True,
                    'filepath': filepath,
                    'file_size': file_size
                }

        return {
            'success': False,
            'error': 'لم يتم العثور على الملف المحمل'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'خطأ في التحميل: {str(e)}'
        }

def cleanup_old_files():
    """Clean up old downloaded files (older than 24 hours)"""
    try:
        downloads_dir = app.config['UPLOAD_FOLDER']
        if not os.path.exists(downloads_dir):
            return

        cutoff_time = time.time() - (24 * 60 * 60)  # 24 hours ago

        for filename in os.listdir(downloads_dir):
            filepath = os.path.join(downloads_dir, filename)
            if os.path.isfile(filepath):
                file_time = os.path.getctime(filepath)
                if file_time < cutoff_time:
                    try:
                        os.remove(filepath)
                        app.logger.info(f"Cleaned up old file: {filename}")
                    except Exception as e:
                        app.logger.error(f"Error removing file {filename}: {str(e)}")

    except Exception as e:
        app.logger.error(f"Error during cleanup: {str(e)}")
