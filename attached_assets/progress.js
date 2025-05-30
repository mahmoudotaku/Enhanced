// Enhanced Progress Tracker for Video Download
class EnhancedProgressTracker {
    constructor() {
        this.downloadId = null;
        this.isTracking = false;
        this.progressInterval = null;
        this.notifications = [];
    }

    // Start tracking download progress
    startTracking(downloadId) {
        this.downloadId = downloadId;
        this.isTracking = true;

        // Show progress card
        const progressCard = document.getElementById('progressCard');
        if (progressCard) {
            progressCard.style.display = 'block';
            progressCard.scrollIntoView({ behavior: 'smooth' });
        }

        // Start polling for progress
        this.progressInterval = setInterval(() => {
            this.updateProgress();
        }, 1000);

        this.updateProgress();
    }

    // Update progress from server
    async updateProgress() {
        if (!this.downloadId || !this.isTracking) {
            return;
        }

        try {
            const response = await fetch(`/api/progress/${this.downloadId}`);
            const data = await response.json();

            if (data.success) {
                const progress = data.progress;
                this.displayProgress(progress);

                // Check if completed or failed
                if (progress.status === 'completed') {
                    this.onDownloadComplete(progress);
                } else if (progress.status === 'failed') {
                    this.onDownloadFailed(progress);
                }
            }
        } catch (error) {
            console.error('Error updating progress:', error);
        }
    }

    // Display progress in UI
    displayProgress(progress) {
        const progressBar = document.getElementById('progressBar');
        const progressStatus = document.getElementById('progressStatus');

        if (progressBar) {
            progressBar.style.width = `${progress.progress}%`;
            progressBar.setAttribute('aria-valuenow', progress.progress);
            progressBar.textContent = `${Math.round(progress.progress)}%`;
        }

        if (progressStatus) {
            progressStatus.textContent = progress.current_step || 'جاري المعالجة...';
        }

        // Update progress bar color based on status
        if (progressBar) {
            progressBar.className = 'progress-bar progress-bar-animated';

            if (progress.status === 'completed') {
                progressBar.classList.add('bg-success');
            } else if (progress.status === 'failed') {
                progressBar.classList.add('bg-danger');
            } else {
                progressBar.classList.add('bg-primary');
            }
        }
    }

    // Handle download completion
    onDownloadComplete(progress) {
        this.stopTracking();

        // Show download button
        const downloadBtn = document.getElementById('downloadFileBtn');
        if (downloadBtn) {
            downloadBtn.style.display = 'block';
            downloadBtn.onclick = () => {
                window.location.href = `/api/download/${this.downloadId}/file`;
            };
        }

        // Show success message
        if (window.VideoDownloader && window.VideoDownloader.showAlert) {
            window.VideoDownloader.showAlert('تم التحميل بنجاح!', 'success');
        }

        // Update status
        const progressStatus = document.getElementById('progressStatus');
        if (progressStatus) {
            progressStatus.innerHTML = '<i class="fas fa-check-circle me-2"></i>تم التحميل بنجاح';
        }
    }

    // Handle download failure
    onDownloadFailed(progress) {
        this.stopTracking();

        // Show error message
        const errorMessage = progress.error_message || 'حدث خطأ أثناء التحميل';
        if (window.VideoDownloader && window.VideoDownloader.showAlert) {
            window.VideoDownloader.showAlert(errorMessage, 'danger');
        }

        // Update status
        const progressStatus = document.getElementById('progressStatus');
        if (progressStatus) {
            progressStatus.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>${errorMessage}`;
        }
    }

    // Stop tracking progress
    stopTracking() {
        this.isTracking = false;
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    // Reset progress card
    reset() {
        this.stopTracking();
        this.downloadId = null;

        const progressCard = document.getElementById('progressCard');
        if (progressCard) {
            progressCard.style.display = 'none';
        }

        const downloadBtn = document.getElementById('downloadFileBtn');
        if (downloadBtn) {
            downloadBtn.style.display = 'none';
        }

        const progressBar = document.getElementById('progressBar');
        if (progressBar) {
            progressBar.style.width = '0%';
            progressBar.setAttribute('aria-valuenow', 0);
            progressBar.textContent = '0%';
            progressBar.className = 'progress-bar progress-bar-animated';
        }

        const progressStatus = document.getElementById('progressStatus');
        if (progressStatus) {
            progressStatus.textContent = 'جاري البدء...';
        }
    }
}

// Global function to start progress tracking
function startProgressTracking(downloadId) {
    if (!window.progressTracker) {
        window.progressTracker = new EnhancedProgressTracker();
    }

    window.progressTracker.reset();
    window.progressTracker.startTracking(downloadId);
}

// Export for use in other files
if (typeof window !== 'undefined') {
    window.startProgressTracking = startProgressTracking;
    window.EnhancedProgressTracker = EnhancedProgressTracker;
}

// Auto-cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.progressTracker) {
        window.progressTracker.stopTracking();
    }
});