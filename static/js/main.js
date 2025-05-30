// Enhanced Video Downloader JavaScript
class VideoDownloader {
    constructor() {
        this.init();
    }

    init() {
        this.setupThemeToggle();
        this.setupFormValidation();
        this.setupEventListeners();
        this.loadTheme();
    }

    // Theme Management
    setupThemeToggle() {
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');

        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = document.body.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                
                document.body.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
                
                // Update icon
                if (themeIcon) {
                    themeIcon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
                }
                
                this.animateThemeChange();
            });
        }
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        const themeIcon = document.getElementById('themeIcon');
        
        document.body.setAttribute('data-theme', savedTheme);
        
        if (themeIcon) {
            themeIcon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    animateThemeChange() {
        document.body.style.transition = 'all 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    // Form Validation
    setupFormValidation() {
        const urlInput = document.getElementById('videoUrl');
        const urlError = document.getElementById('urlError');

        if (urlInput) {
            urlInput.addEventListener('input', () => {
                this.validateUrl(urlInput.value, urlError);
            });

            urlInput.addEventListener('paste', (e) => {
                setTimeout(() => {
                    this.validateUrl(urlInput.value, urlError);
                }, 10);
            });
        }
    }

    validateUrl(url, errorElement) {
        const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
        const isValid = urlPattern.test(url.trim());

        if (errorElement) {
            if (url && !isValid) {
                errorElement.textContent = 'يرجى إدخال رابط صحيح';
                errorElement.style.display = 'block';
                return false;
            } else {
                errorElement.style.display = 'none';
                return true;
            }
        }

        return isValid;
    }

    // Event Listeners
    setupEventListeners() {
        // Auto-cleanup on page load
        this.scheduleCleanup();
        
        // Handle form submissions
        this.setupDownloadForm();
        
        // Handle keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                const downloadBtn = document.getElementById('downloadBtn');
                if (downloadBtn && !downloadBtn.disabled) {
                    downloadBtn.click();
                }
            }
        });
    }

    setupDownloadForm() {
        const form = document.getElementById('downloadForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleDownload();
            });
        }
    }

    // Download Handling
    async handleDownload() {
        const urlInput = document.getElementById('videoUrl');
        const qualitySelect = document.getElementById('qualitySelect');
        const downloadBtn = document.getElementById('downloadBtn');

        if (!urlInput || !qualitySelect || !downloadBtn) return;

        const url = urlInput.value.trim();
        const quality = qualitySelect.value;

        if (!url) {
            this.showAlert('يرجى إدخال رابط الفيديو', 'warning');
            return;
        }

        if (!this.validateUrl(url)) {
            this.showAlert('يرجى إدخال رابط صحيح', 'warning');
            return;
        }

        try {
            downloadBtn.disabled = true;
            downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>جاري البدء...';

            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url, quality: quality })
            });

            const data = await response.json();

            if (data.success) {
                if (window.startProgressTracking) {
                    window.startProgressTracking(data.download_id);
                }
                this.showAlert('تم بدء عملية التحميل', 'success');
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            console.error('Download error:', error);
            this.showAlert('خطأ في الشبكة. يرجى المحاولة مرة أخرى.', 'danger');
        } finally {
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = '<i class="fas fa-download me-2"></i>تحميل الآن';
        }
    }

    // Video Preview
    async showVideoPreview(data) {
        const previewCard = document.getElementById('videoPreview');
        if (!previewCard) return;

        // Update preview data
        this.updateElement('videoTitle', data.title);
        this.updateElement('videoChannel', data.channel);
        this.updateElement('videoDuration', data.duration);
        this.updateElement('videoViews', this.formatNumber(data.view_count));
        this.updateElement('videoDate', data.upload_date);

        // Update thumbnail
        const thumbnail = document.getElementById('videoThumbnail');
        if (thumbnail && data.thumbnail) {
            thumbnail.src = data.thumbnail;
            thumbnail.alt = data.title;
        }

        // Show preview card with animation
        previewCard.style.display = 'block';
        previewCard.scrollIntoView({ behavior: 'smooth' });
    }

    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value || 'غير محدد';
        }
    }

    // Utility Functions
    formatNumber(num) {
        if (!num) return '0';
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    showAlert(message, type = 'info') {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.temp-alert');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show temp-alert`;
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '100px';
        alertDiv.style.right = '20px';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.minWidth = '300px';
        alertDiv.style.maxWidth = '500px';

        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertDiv);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Cleanup Functions
    scheduleCleanup() {
        // Run cleanup every hour
        setInterval(() => {
            this.performCleanup();
        }, 60 * 60 * 1000);
    }

    async performCleanup() {
        try {
            const response = await fetch('/api/cleanup');
            const data = await response.json();
            console.log('Cleanup result:', data);
        } catch (error) {
            console.error('Cleanup error:', error);
        }
    }

    // URL Detection and Auto-fill
    detectAndFillUrl() {
        const urlInput = document.getElementById('videoUrl');
        if (urlInput && !urlInput.value) {
            // Check clipboard for URLs (requires user interaction)
            if (navigator.clipboard && navigator.clipboard.readText) {
                navigator.clipboard.readText().then(text => {
                    if (this.validateUrl(text)) {
                        urlInput.value = text;
                        this.showAlert('تم اكتشاف رابط في الحافظة', 'info');
                    }
                }).catch(() => {
                    // Clipboard access denied or not available
                });
            }
        }
    }
}

// Global functions for backward compatibility
window.VideoDownloader = VideoDownloader;

window.showVideoPreview = function(data) {
    if (window.videoDownloader) {
        window.videoDownloader.showVideoPreview(data);
    }
};

window.showAlert = function(message, type) {
    if (window.videoDownloader) {
        window.videoDownloader.showAlert(message, type);
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.videoDownloader = new VideoDownloader();
    
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add loading animation to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
            }
        });
    });

    // Add intersection observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.platform-card, .feature-item').forEach(el => {
        observer.observe(el);
    });
});

// Service Worker Registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Handle online/offline status
window.addEventListener('online', () => {
    if (window.videoDownloader) {
        window.videoDownloader.showAlert('تم استعادة الاتصال بالإنترنت', 'success');
    }
});

window.addEventListener('offline', () => {
    if (window.videoDownloader) {
        window.videoDownloader.showAlert('تم فقدان الاتصال بالإنترنت', 'warning');
    }
});
