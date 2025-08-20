import os
import re
import uuid
import time
import yt_dlp
from datetime import datetime, timedelta
from urllib.parse import urlparse
from app import app

def generate_download_id():
    """Generate a unique download ID"""
    return str(uuid.uuid4())[:8]

def get_platform_name(url):
    """Extract platform name from URL"""
    domain = urlparse(url).netloc.lower()
    
    if 'youtube.com' in domain or 'youtu.be' in domain:
        return 'YouTube'
    elif 'tiktok.com' in domain:
        return 'TikTok'
    elif 'instagram.com' in domain:
        return 'Instagram'
    elif 'twitter.com' in domain or 'x.com' in domain:
        return 'Twitter'
    elif 'facebook.com' in domain or 'fb.watch' in domain:
        return 'Facebook'
    elif 'vimeo.com' in domain:
        return 'Vimeo'
    elif 'dailymotion.com' in domain:
        return 'Dailymotion'
    else:
        return 'أخرى'

def format_duration(seconds):
    """Format duration from seconds to readable format"""
    if not seconds:
        return 'غير محدد'
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def format_file_size(bytes_size):
    """Format file size from bytes to readable format"""
    if not bytes_size:
        return 'غير محدد'
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def get_video_info(url):
    """Get video information using yt-dlp"""
    try:
        # Enhanced options for better compatibility
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        # Special handling for Facebook
        if 'facebook.com' in url or 'fb.watch' in url:
            ydl_opts.update({
                'extractor_args': {
                    'facebook': {
                        'api_version': 'v18.0'
                    }
                }
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'success': True,
                'data': info
            }
            
    except yt_dlp.DownloadError as e:
        error_msg = str(e)
        if 'Video unavailable' in error_msg:
            error_msg = 'الفيديو غير متوفر أو تم حذفه'
        elif 'Private video' in error_msg:
            error_msg = 'الفيديو خاص ولا يمكن الوصول إليه'
        elif 'age-restricted' in error_msg:
            error_msg = 'الفيديو مقيد بالعمر'
        elif 'Cannot parse data' in error_msg:
            error_msg = 'المنصة لا تدعم هذا النوع من الروابط حالياً'
        elif 'Requested format is not available' in error_msg:
            error_msg = 'جودة الفيديو المطلوبة غير متوفرة'
        elif 'facebook' in error_msg.lower():
            error_msg = 'مشكلة في الوصول لفيديو فيسبوك. جرب رابط مختلف أو منصة أخرى'
        else:
            error_msg = 'فشل في الحصول على معلومات الفيديو'
            
        return {
            'success': False,
            'error': error_msg
        }
    except Exception as e:
        app.logger.error(f"Error extracting video info: {str(e)}")
        return {
            'success': False,
            'error': 'خطأ في معالجة الرابط. تأكد من صحة الرابط.'
        }

def download_video(url, quality, download_id, progress_callback=None):
    """Download video using yt-dlp"""
    try:
        downloads_dir = app.config['UPLOAD_FOLDER']
        os.makedirs(downloads_dir, exist_ok=True)
        
        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(downloads_dir, f'{download_id}_%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extractaudio': quality == 'mp3',
            'audioformat': 'mp3' if quality == 'mp3' else None,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'retries': 3,
            'ignoreerrors': False,
        }
        
        # Special handling for Facebook
        if 'facebook.com' in url or 'fb.watch' in url:
            ydl_opts.update({
                'extractor_args': {
                    'facebook': {
                        'api_version': 'v18.0'
                    }
                },
                # For Facebook, try more flexible format selection
                'format': 'best[height<=720]/best' if quality != 'mp3' else 'bestaudio/best'
            })
        
        # Set video quality for non-Facebook URLs
        if 'facebook.com' not in url and 'fb.watch' not in url:
            if quality == 'best':
                ydl_opts['format'] = 'best[height<=1080]/best'
            elif quality == 'mp3':
                ydl_opts['format'] = 'bestaudio/best'
            elif quality in ['1080p', '720p', '480p', '360p', '240p', '144p']:
                # Extract height from quality (e.g., "720p" -> 720)
                height = int(quality.replace('p', ''))
                ydl_opts['format'] = f'best[height<={height}]/worst[height>={height}]/best'
            else:
                # Fallback to best quality
                ydl_opts['format'] = 'best[height<=1080]/best'
        
        # Add progress hook if callback provided
        if progress_callback:
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if 'total_bytes' in d and d['total_bytes']:
                        percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                        progress_callback(percent)
                    elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                        percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                        progress_callback(percent)
            
            ydl_opts['progress_hooks'] = [progress_hook]
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find the downloaded file
        downloaded_file = None
        for filename in os.listdir(downloads_dir):
            if filename.startswith(f'{download_id}_'):
                downloaded_file = os.path.join(downloads_dir, filename)
                break
        
        if downloaded_file and os.path.exists(downloaded_file):
            file_size = os.path.getsize(downloaded_file)
            return {
                'success': True,
                'filepath': downloaded_file,
                'file_size': file_size
            }
        else:
            return {
                'success': False,
                'error': 'فشل في حفظ الملف'
            }
            
    except yt_dlp.DownloadError as e:
        error_msg = str(e)
        if 'Video unavailable' in error_msg:
            error_msg = 'الفيديو غير متوفر للتحميل'
        elif 'format not available' in error_msg or 'Requested format is not available' in error_msg:
            error_msg = 'الجودة المطلوبة غير متوفرة. جرب جودة أخرى'
        elif 'Cannot parse data' in error_msg:
            error_msg = 'فشل في تحليل بيانات الفيديو. جرب رابط آخر'
        elif 'facebook' in error_msg.lower():
            error_msg = 'فيسبوك يواجه مشاكل حالياً. جرب يوتيوب أو منصة أخرى'
        elif 'Private video' in error_msg:
            error_msg = 'الفيديو خاص ولا يمكن تحميله'
        elif 'age-restricted' in error_msg:
            error_msg = 'الفيديو مقيد بالعمر ولا يمكن تحميله'
        else:
            error_msg = 'فشل في تحميل الفيديو'
            
        return {
            'success': False,
            'error': error_msg
        }
    except Exception as e:
        app.logger.error(f"Error downloading video: {str(e)}")
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

def sanitize_filename(filename):
    """Sanitize filename for safe file system storage"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    filename = filename[:100]
    return filename
