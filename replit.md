# Arabic Video Downloader

## Overview

This is a comprehensive Arabic video downloader web application built with Flask that allows users to download videos from over 1000 platforms including YouTube, TikTok, Instagram, Facebook, and Twitter. The application features a modern Glass Morphism design with full Arabic RTL support and both light and dark themes.

## System Architecture

### Frontend Architecture
- **Framework**: Pure HTML/CSS/JavaScript with Bootstrap 5
- **Design System**: Glass Morphism with Arabic RTL support
- **Theming**: Light/Dark theme toggle with CSS variables
- **Responsive Design**: Mobile-first approach with Bootstrap grid system
- **Fonts**: Google Fonts (Cairo) for Arabic typography
- **Icons**: Font Awesome for UI elements

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Video Processing**: yt-dlp library for video extraction
- **Media Processing**: FFmpeg for video/audio conversion
- **Session Management**: Flask sessions with configurable secret key
- **Deployment**: Gunicorn WSGI server with proxy fix middleware

## Key Components

### Database Models
- **DownloadHistory**: Tracks completed downloads with metadata (title, quality, file size, platform, etc.)
- **DownloadProgress**: Real-time progress tracking for active downloads

### Core Utilities
- **Video Information Extraction**: yt-dlp integration for metadata retrieval
- **Download Management**: Asynchronous download processing with progress tracking
- **File Management**: Automatic cleanup of old downloads
- **Platform Detection**: URL analysis to identify video platforms

### API Endpoints
- `GET /`: Main application interface
- `GET /history`: Download history page
- `POST /api/info`: Get video information
- `POST /api/download`: Initiate video download
- `GET /api/progress/{id}`: Real-time download progress

## Data Flow

1. **User Input**: User enters video URL and selects quality preferences
2. **Validation**: Frontend validates URL format and requirements
3. **Information Extraction**: Backend uses yt-dlp to extract video metadata
4. **Preview Display**: Frontend shows video information for user confirmation
5. **Download Initiation**: Backend starts download process with progress tracking
6. **Progress Monitoring**: Real-time updates via AJAX polling
7. **File Delivery**: Completed downloads served via secure file transfer
8. **History Logging**: Download details stored in database for future reference

## External Dependencies

### Python Libraries
- **Flask**: Web framework and routing
- **SQLAlchemy**: Database ORM and migrations
- **yt-dlp**: Video extraction from 1000+ platforms
- **ffmpeg-python**: Video/audio processing
- **gunicorn**: Production WSGI server
- **psycopg2-binary**: PostgreSQL database adapter

### Frontend Libraries
- **Bootstrap 5**: UI framework with RTL support
- **Font Awesome**: Icon library
- **Google Fonts**: Arabic typography (Cairo font family)

### System Dependencies
- **FFmpeg**: Media processing and conversion
- **PostgreSQL**: Production database (SQLite for development)
- **OpenSSL**: Secure connections and encryption

## Deployment Strategy

### Production Environment
- **Platform**: Heroku with auto-scaling
- **Database**: Heroku PostgreSQL (essential-0 plan)
- **Buildpacks**: 
  - FFmpeg buildpack for media processing
  - Python buildpack for Flask application
- **Process Types**: Web dynos with Gunicorn
- **Environment Variables**: Secure configuration management

### Development Environment
- **Database**: SQLite for local development
- **Server**: Flask development server
- **Hot Reload**: Automatic code reloading enabled
- **Debug Mode**: Enhanced error reporting

### Container Support
- **Docker**: Multi-stage build with Python 3.11 slim base
- **Health Checks**: Built-in endpoint monitoring
- **Security**: Non-root user execution
- **Optimization**: Minimal image size with dependency caching

## Changelog

- June 14, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.