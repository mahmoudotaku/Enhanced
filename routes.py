from flask import render_template, request, jsonify, send_file, flash, redirect, url_for
from app import app, db
from models import DownloadHistory, DownloadProgress
from utils import (
    get_video_info, download_video, generate_download_id, 
    format_file_size, format_duration, get_platform_name,
    cleanup_old_files
)
import os
import threading
from datetime import datetime, timedelta

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/history')
def history():
    """Download history page"""
    # Get recent downloads (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    downloads = DownloadHistory.query.filter(
        DownloadHistory.download_date >= thirty_days_ago
    ).order_by(DownloadHistory.download_date.desc()).limit(50).all()
    
    return render_template('history.html', downloads=downloads)

@app.route('/api/info', methods=['POST'])
def api_get_info():
    """Get video information via API"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'success': False, 'error': 'لم يتم توفير رابط الفيديو'})
        
        url = data['url'].strip()
        if not url:
            return jsonify({'success': False, 'error': 'رابط الفيديو فارغ'})
        
        # Get video information
        info = get_video_info(url)
        if not info['success']:
            return jsonify(info)
        
        # Format the response
        video_info = info['data']
        response = {
            'success': True,
            'title': video_info.get('title', 'غير محدد'),
            'duration': format_duration(video_info.get('duration', 0)),
            'view_count': video_info.get('view_count', 0),
            'channel': video_info.get('uploader', 'غير محدد'),
            'upload_date': video_info.get('upload_date', 'غير محدد'),
            'thumbnail': video_info.get('thumbnail', ''),
            'platform': get_platform_name(url),
            'available_formats': []
        }
        
        # Add available formats information
        formats = video_info.get('formats', [])
        quality_map = {}
        
        for fmt in formats:
            if fmt.get('vcodec') != 'none' and fmt.get('height'):
                height = fmt['height']
                quality = f"{height}p"
                if quality not in quality_map:
                    quality_map[quality] = {
                        'quality': quality,
                        'filesize': fmt.get('filesize') or fmt.get('filesize_approx', 0)
                    }
        
        # Sort by quality
        sorted_qualities = sorted(quality_map.items(), key=lambda x: int(x[0][:-1]), reverse=True)
        response['available_formats'] = [item[1] for item in sorted_qualities]
        
        return jsonify(response)
        
    except Exception as e:
        app.logger.error(f"Error getting video info: {str(e)}")
        return jsonify({'success': False, 'error': f'خطأ في الحصول على معلومات الفيديو: {str(e)}'})

@app.route('/api/download', methods=['POST'])
def api_download():
    """Start download process via API"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'success': False, 'error': 'لم يتم توفير رابط الفيديو'})
        
        url = data['url'].strip()
        quality = data.get('quality', 'best')
        
        if not url:
            return jsonify({'success': False, 'error': 'رابط الفيديو فارغ'})
        
        # Generate unique download ID
        download_id = generate_download_id()
        
        # Create progress tracker
        progress = DownloadProgress(
            download_id=download_id,
            status='queued',
            current_step='في الانتظار...'
        )
        db.session.add(progress)
        db.session.commit()
        
        # Start download in background thread
        download_thread = threading.Thread(
            target=download_video_background,
            args=(download_id, url, quality)
        )
        download_thread.daemon = True
        download_thread.start()
        
        return jsonify({
            'success': True,
            'download_id': download_id,
            'message': 'تم بدء عملية التحميل'
        })
        
    except Exception as e:
        app.logger.error(f"Error starting download: {str(e)}")
        return jsonify({'success': False, 'error': f'خطأ في بدء التحميل: {str(e)}'})

@app.route('/api/progress/<download_id>')
def api_get_progress(download_id):
    """Get download progress"""
    try:
        progress = DownloadProgress.query.filter_by(download_id=download_id).first()
        if not progress:
            return jsonify({'success': False, 'error': 'معرف التحميل غير صحيح'})
        
        return jsonify({
            'success': True,
            'progress': progress.to_dict()
        })
        
    except Exception as e:
        app.logger.error(f"Error getting progress: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/download/<download_id>/file')
def api_download_file(download_id):
    """Download the completed file"""
    try:
        # Find the download progress record
        progress = DownloadProgress.query.filter_by(download_id=download_id).first()
        if not progress or progress.status != 'completed':
            return jsonify({'success': False, 'error': 'الملف غير متوفر للتحميل'})
        
        # Look for the file in downloads directory
        downloads_dir = app.config['UPLOAD_FOLDER']
        
        # Find the actual file (it might have different extension)
        for filename in os.listdir(downloads_dir):
            if filename.startswith(f"{download_id}_"):
                filepath = os.path.join(downloads_dir, filename)
                if os.path.exists(filepath):
                    # Clean the filename for download
                    original_name = filename[len(f"{download_id}_"):]
                    safe_name = ''.join(c for c in original_name if c.isalnum() or c in '._- ')
                    
                    return send_file(
                        filepath,
                        as_attachment=True,
                        download_name=safe_name or 'video.mp4'
                    )
        
        return jsonify({'success': False, 'error': 'الملف غير موجود'})
        
    except Exception as e:
        app.logger.error(f"Error downloading file: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/history')
def api_get_history():
    """Get download history via API"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        downloads = DownloadHistory.query.order_by(
            DownloadHistory.download_date.desc()
        ).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'downloads': [download.to_dict() for download in downloads.items],
            'total': downloads.total,
            'pages': downloads.pages,
            'current_page': page
        })
        
    except Exception as e:
        app.logger.error(f"Error getting history: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/history/clear', methods=['DELETE'])
def api_clear_history():
    """Clear download history"""
    try:
        DownloadHistory.query.delete()
        DownloadProgress.query.delete()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم مسح السجل بنجاح'})
    except Exception as e:
        app.logger.error(f"Error clearing history: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/cleanup')
def api_cleanup():
    """Cleanup old downloaded files"""
    try:
        cleanup_old_files()
        return jsonify({'success': True, 'message': 'تم تنظيف الملفات القديمة'})
    except Exception as e:
        app.logger.error(f"Error during cleanup: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

def download_video_background(download_id, url, quality):
    """Background function to handle video download"""
    try:
        # Update progress to downloading
        progress = DownloadProgress.query.filter_by(download_id=download_id).first()
        if not progress:
            return
        
        progress.status = 'downloading'
        progress.current_step = 'جاري الحصول على معلومات الفيديو...'
        progress.progress = 10.0
        db.session.commit()
        
        # Get video info first
        info_result = get_video_info(url)
        if not info_result['success']:
            progress.status = 'failed'
            progress.error_message = info_result['error']
            db.session.commit()
            return
        
        video_info = info_result['data']
        
        # Update progress
        progress.current_step = 'جاري تحميل الفيديو...'
        progress.progress = 30.0
        db.session.commit()
        
        # Download the video
        download_result = download_video(
            url, quality, download_id, 
            lambda p: update_download_progress(download_id, p)
        )
        
        if download_result['success']:
            # Save to history
            history = DownloadHistory(
                url=url,
                title=video_info.get('title', 'غير محدد'),
                quality=quality,
                file_size=download_result.get('file_size', 0),
                duration=video_info.get('duration', 0),
                platform=get_platform_name(url),
                status='completed',
                thumbnail_url=video_info.get('thumbnail', ''),
                channel_name=video_info.get('uploader', ''),
                view_count=video_info.get('view_count', 0),
                upload_date=video_info.get('upload_date', '')
            )
            db.session.add(history)
            
            # Update progress to completed
            progress.status = 'completed'
            progress.current_step = 'تم التحميل بنجاح'
            progress.progress = 100.0
            db.session.commit()
            
        else:
            # Update progress to failed
            progress.status = 'failed'
            progress.error_message = download_result['error']
            db.session.commit()
            
    except Exception as e:
        app.logger.error(f"Error in background download: {str(e)}")
        try:
            progress = DownloadProgress.query.filter_by(download_id=download_id).first()
            if progress:
                progress.status = 'failed'
                progress.error_message = str(e)
                db.session.commit()
        except:
            pass

def update_download_progress(download_id, progress_percent):
    """Update download progress in database"""
    try:
        progress = DownloadProgress.query.filter_by(download_id=download_id).first()
        if progress:
            progress.progress = 30.0 + (progress_percent * 0.7)  # 30-100% range
            progress.current_step = f'جاري التحميل... {progress_percent:.1f}%'
            db.session.commit()
    except Exception as e:
        app.logger.error(f"Error updating progress: {str(e)}")
