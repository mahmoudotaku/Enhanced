from datetime import datetime
from app import db

class DownloadHistory(db.Model):
    """Model to store download history"""
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    quality = db.Column(db.String(20), nullable=False)
    file_size = db.Column(db.Integer)  # Size in bytes
    duration = db.Column(db.Integer)  # Duration in seconds
    platform = db.Column(db.String(50))  # YouTube, TikTok, etc.
    download_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')  # completed, failed, in_progress
    error_message = db.Column(db.Text)
    thumbnail_url = db.Column(db.Text)
    channel_name = db.Column(db.String(200))
    view_count = db.Column(db.Integer)
    upload_date = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<DownloadHistory {self.title}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'quality': self.quality,
            'file_size': self.file_size,
            'duration': self.duration,
            'platform': self.platform,
            'download_date': self.download_date.isoformat() if self.download_date else None,
            'status': self.status,
            'error_message': self.error_message,
            'thumbnail_url': self.thumbnail_url,
            'channel_name': self.channel_name,
            'view_count': self.view_count,
            'upload_date': self.upload_date
        }

class DownloadProgress(db.Model):
    """Model to track download progress"""
    id = db.Column(db.Integer, primary_key=True)
    download_id = db.Column(db.String(50), unique=True, nullable=False)
    progress = db.Column(db.Float, default=0.0)  # Progress percentage
    status = db.Column(db.String(20), default='queued')  # queued, downloading, completed, failed
    current_step = db.Column(db.String(100))  # Current operation description
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DownloadProgress {self.download_id}>'
    
    def to_dict(self):
        return {
            'download_id': self.download_id,
            'progress': self.progress,
            'status': self.status,
            'current_step': self.current_step,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
