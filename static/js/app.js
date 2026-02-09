// API Base URL
const API_BASE = '/api';

// State
let currentFilter = 'all';
let jobs = [];
let refreshInterval;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    loadJobs();
    loadStatus();
    setupEventListeners();
    startAutoRefresh();
});

// Setup event listeners
function setupEventListeners() {
    // Settings form
    document.getElementById('settingsForm').addEventListener('submit', saveSettings);

    // CRF slider
    const crfSlider = document.getElementById('crf');
    const crfValue = document.getElementById('crfValue');
    crfSlider.addEventListener('input', (e) => {
        crfValue.textContent = e.target.value;
    });

    // Scan button
    document.getElementById('scanBtn').addEventListener('click', scanFolder);

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            renderJobs();
        });
    });
}

// Load settings
async function loadSettings() {
    try {
        const response = await fetch(`${API_BASE}/settings`);
        const settings = await response.json();

        document.getElementById('sourceFolder').value = settings.source_folder || '';
        document.getElementById('outputFolder').value = settings.output_folder || '';
        document.getElementById('outputFormat').value = settings.output_format || 'mp4';
        document.getElementById('videoCodec').value = settings.video_codec || 'libx264';
        document.getElementById('audioCodec').value = settings.audio_codec || 'aac';
        document.getElementById('preset').value = settings.preset || 'medium';
        document.getElementById('crf').value = settings.crf || 23;
        document.getElementById('crfValue').textContent = settings.crf || 23;
        document.getElementById('watchEnabled').checked = settings.watch_enabled || false;
    } catch (error) {
        showNotification('Failed to load settings', 'error');
        console.error('Error loading settings:', error);
    }
}

// Save settings
async function saveSettings(e) {
    e.preventDefault();

    const settings = {
        source_folder: document.getElementById('sourceFolder').value,
        output_folder: document.getElementById('outputFolder').value,
        output_format: document.getElementById('outputFormat').value,
        video_codec: document.getElementById('videoCodec').value,
        audio_codec: document.getElementById('audioCodec').value,
        preset: document.getElementById('preset').value,
        crf: parseInt(document.getElementById('crf').value),
        watch_enabled: document.getElementById('watchEnabled').checked
    };

    try {
        const response = await fetch(`${API_BASE}/settings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });

        if (response.ok) {
            showNotification('Settings saved successfully', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to save settings', 'error');
        }
    } catch (error) {
        showNotification('Failed to save settings', 'error');
        console.error('Error saving settings:', error);
    }
}

// Scan folder for new videos
async function scanFolder() {
    try {
        const response = await fetch(`${API_BASE}/scan`, {
            method: 'POST'
        });

        if (response.ok) {
            const result = await response.json();
            showNotification(result.message, 'success');
            loadJobs();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to scan folder', 'error');
        }
    } catch (error) {
        showNotification('Failed to scan folder', 'error');
        console.error('Error scanning folder:', error);
    }
}

// Load jobs
async function loadJobs() {
    try {
        const response = await fetch(`${API_BASE}/jobs`);
        jobs = await response.json();
        renderJobs();
    } catch (error) {
        console.error('Error loading jobs:', error);
    }
}

// Render jobs
function renderJobs() {
    const jobsList = document.getElementById('jobsList');

    // Filter jobs
    let filteredJobs = jobs;
    if (currentFilter !== 'all') {
        filteredJobs = jobs.filter(job => job.status === currentFilter);
    }

    if (filteredJobs.length === 0) {
        jobsList.innerHTML = '<p class="empty-state">No jobs found.</p>';
        return;
    }

    jobsList.innerHTML = filteredJobs.map(job => `
        <div class="job-item">
            <div class="job-header">
                <div class="job-info">
                    <h3>${getFileName(job.source_file)}</h3>
                    <p>${job.source_file}</p>
                    ${job.output_file ? `<p>Output: ${job.output_file}</p>` : ''}
                    <p>Created: ${formatDate(job.created_at)}</p>
                </div>
                <div class="job-status">
                    <span class="status-badge status-${job.status}">${job.status.toUpperCase()}</span>
                    ${job.status !== 'processing' ? `
                        <button class="btn btn-danger" onclick="deleteJob(${job.id})">Delete</button>
                    ` : ''}
                </div>
            </div>
            
            ${job.status === 'processing' ? `
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${job.progress}%"></div>
                    </div>
                    <p class="progress-text">${job.progress.toFixed(1)}% complete</p>
                </div>
            ` : ''}
            
            ${job.error_message ? `
                <div class="error-message">
                    Error: ${job.error_message}
                </div>
            ` : ''}
        </div>
    `).join('');
}

// Delete job
async function deleteJob(jobId) {
    if (!confirm('Are you sure you want to delete this job?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/jobs/${jobId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showNotification('Job deleted successfully', 'success');
            loadJobs();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to delete job', 'error');
        }
    } catch (error) {
        showNotification('Failed to delete job', 'error');
        console.error('Error deleting job:', error);
    }
}

// Load system status
async function loadStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const status = await response.json();

        document.getElementById('cpuUsage').textContent = `${status.cpu_percent.toFixed(1)}%`;
        document.getElementById('memoryUsage').textContent = `${status.memory_percent.toFixed(1)}%`;
        document.getElementById('totalJobs').textContent = status.total_jobs;
        document.getElementById('processingJobs').textContent = status.processing_jobs;
    } catch (error) {
        console.error('Error loading status:', error);
    }
}

// Auto-refresh
function startAutoRefresh() {
    refreshInterval = setInterval(() => {
        loadJobs();
        loadStatus();
    }, 3000); // Refresh every 3 seconds
}

// Utility functions
function getFileName(path) {
    return path.split('/').pop();
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});