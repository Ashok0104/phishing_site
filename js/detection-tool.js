document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const analysisForm = document.querySelector('.analysis-form');
    const urlInput = document.querySelector('#url-input');
    const resultsContainer = document.querySelector('.results-container');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const analysisResults = document.querySelector('.analysis-results');
    const resultStatus = document.querySelector('.result-status');
    const statusIcon = document.querySelector('.status-icon');
    const statusText = document.querySelector('.status-text');
    const scoreValue = document.querySelector('.score-value');
    const scoreLabel = document.querySelector('.score-label');
    const scoreBars = document.querySelectorAll('.score-fill');
    const saveReportBtn = document.querySelector('#save-report');
    const shareResultsBtn = document.querySelector('#share-results');

    // Form submission
    analysisForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        if (!url) {
            showError('Please enter a URL to analyze');
            return;
        }

        // Show loading spinner
        loadingSpinner.style.display = 'flex';
        analysisResults.classList.remove('show');

        try {
            // Simulate API call (replace with actual API endpoint)
            const response = await analyzeUrl(url);
            
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            
            // Update results
            updateResults(response);
            
            // Show results with animation
            analysisResults.classList.add('show');
        } catch (error) {
            loadingSpinner.style.display = 'none';
            showError('An error occurred while analyzing the URL');
            console.error('Analysis error:', error);
        }
    });

    // URL analysis function (simulated)
    async function analyzeUrl(url) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Simulated response (replace with actual API response)
        return {
            status: 'safe', // or 'unsafe' or 'warning'
            score: 85,
            details: {
                domainAge: '2 years',
                sslStatus: 'Valid',
                ipAddress: '192.168.1.1',
                suspiciousKeywords: ['none'],
                formFields: 'Secure',
                javascriptAnalysis: 'Clean'
            }
        };
    }

    // Update results display
    function updateResults(data) {
        // Update status
        resultStatus.className = 'result-status';
        resultStatus.classList.add(data.status);
        
        // Update status icon and text
        if (data.status === 'safe') {
            statusIcon.innerHTML = '<i class="fas fa-shield-alt"></i>';
            statusText.textContent = 'Safe Website';
        } else if (data.status === 'unsafe') {
            statusIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
            statusText.textContent = 'Unsafe Website';
        } else {
            statusIcon.innerHTML = '<i class="fas fa-exclamation-circle"></i>';
            statusText.textContent = 'Warning';
        }

        // Update score
        scoreValue.textContent = data.score;
        scoreLabel.textContent = 'Reputation Score';

        // Update score bars
        scoreBars.forEach(bar => {
            bar.style.width = `${data.score}%`;
        });

        // Update details
        const detailItems = document.querySelectorAll('.detail-item');
        detailItems.forEach(item => {
            const key = item.dataset.key;
            if (data.details[key]) {
                const valueElement = item.querySelector('.detail-value');
                valueElement.textContent = data.details[key];
            }
        });
    }

    // Show error message
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        // Remove any existing error message
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Insert error message before the form
        analysisForm.parentNode.insertBefore(errorDiv, analysisForm);
        
        // Remove error message after 3 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 3000);
    }

    // Save report functionality
    saveReportBtn.addEventListener('click', function() {
        // Create report data
        const reportData = {
            url: urlInput.value,
            timestamp: new Date().toISOString(),
            score: scoreValue.textContent,
            status: resultStatus.classList.contains('safe') ? 'Safe' : 
                   resultStatus.classList.contains('unsafe') ? 'Unsafe' : 'Warning',
            details: {}
        };

        // Get all details
        const detailItems = document.querySelectorAll('.detail-item');
        detailItems.forEach(item => {
            const key = item.dataset.key;
            const value = item.querySelector('.detail-value').textContent;
            reportData.details[key] = value;
        });

        // Create and download report file
        const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `phishing-report-${new Date().getTime()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    // Share results functionality
    shareResultsBtn.addEventListener('click', function() {
        if (navigator.share) {
            navigator.share({
                title: 'Phishing Detection Results',
                text: `Analysis results for ${urlInput.value}`,
                url: window.location.href
            })
            .catch(error => console.error('Error sharing:', error));
        } else {
            // Fallback for browsers that don't support Web Share API
            const shareUrl = `${window.location.href}?url=${encodeURIComponent(urlInput.value)}`;
            navigator.clipboard.writeText(shareUrl)
                .then(() => {
                    alert('Share link copied to clipboard!');
                })
                .catch(error => {
                    console.error('Error copying to clipboard:', error);
                    alert('Could not copy share link. Please try again.');
                });
        }
    });

    // Add CSS for error message
    const style = document.createElement('style');
    style.textContent = `
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
}); 