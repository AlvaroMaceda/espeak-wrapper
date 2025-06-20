// Main JavaScript for eSpeak Wrapper

document.addEventListener('DOMContentLoaded', function() {
    // Store history of speech items - load from localStorage if available
    let speechHistory = [];

    // Load speech history from localStorage if available
    try {
        const savedHistory = localStorage.getItem('speechHistory');
        if (savedHistory) {
            // Parse stored data - note that audio URLs can't be stored persistently
            // so we'll need to handle that separately
            const parsedHistory = JSON.parse(savedHistory);
            // We'll filter out any items without valid data
            speechHistory = parsedHistory.filter(item => item && item.text);

            // Mark these items as needing audio regeneration
            speechHistory.forEach(item => {
                item.needsRegeneration = true;
                item.audioUrl = null;
            });
        }
    } catch (e) {
        console.error('Error loading speech history:', e);
        // If there's an error loading, start fresh
        speechHistory = [];
    }

    // Function to save history to localStorage
    function saveToLocalStorage() {
        try {
            // Create a copy of the history without the audioUrl (can't be serialized)
            const historyForStorage = speechHistory.map(item => {
                // Create a copy without the audioUrl
                const { audioUrl, ...rest } = item;
                return rest;
            });
            localStorage.setItem('speechHistory', JSON.stringify(historyForStorage));
        } catch (e) {
            console.error('Error saving speech history:', e);
        }
    }

    // Function to clear all history
    function clearAllHistory() {
        speechHistory = [];
        saveToLocalStorage();
        renderSpeechHistory();
    }

    // Function to delete a specific item
    function deleteHistoryItem(index) {
        speechHistory.splice(index, 1);
        saveToLocalStorage();
        renderSpeechHistory();
    }

    // Function to render all speech items
    function renderSpeechHistory() {
        const resultDiv = document.getElementById('result');
        const historyTitle = document.getElementById('historyTitle');

        if (speechHistory.length === 0) {
            resultDiv.innerHTML = '';
            historyTitle.style.display = 'none';
            return;
        }

        historyTitle.style.display = 'block';

        // Add the clear all button to the history title
        if (!document.getElementById('clearAllBtn')) {
            const clearBtn = document.createElement('button');
            clearBtn.id = 'clearAllBtn';
            clearBtn.className = 'clear-all-btn';
            clearBtn.innerHTML = '<i class="fas fa-trash-alt"></i> Clear History';
            clearBtn.addEventListener('click', clearAllHistory);
            historyTitle.appendChild(clearBtn);
        }

        let historyHtml = '';
        speechHistory.forEach((item, index) => {
            // Check if we need to regenerate audio for this item (after page refresh)
            const audioSection = item.needsRegeneration ?
                `<div class="audio-player">
                    <div class="audio-unavailable">
                        <p><i class="fas fa-exclamation-circle"></i> Audio unavailable after page refresh</p>
                        <button class="regenerate-btn" data-index="${index}">
                            <i class="fas fa-sync"></i> Regenerate Audio
                        </button>
                    </div>
                </div>` :
                `<div class="audio-player">
                    <audio controls ${index === 0 ? 'autoplay' : ''}>
                        <source src="${item.audioUrl}" type="audio/wav">
                        Your browser does not support the audio element.
                    </audio>
                </div>
                <a href="${item.audioUrl}" download="speech_${Date.now()}.wav" class="download-link">
                    <i class="fas fa-download"></i> Download audio file
                </a>`;

            historyHtml += `
                <div class="card speech-item" data-index="${index}">
                    <div class="speech-header">
                        <h3 class="result-title">Generated Speech #${speechHistory.length - index}</h3>
                        <button class="delete-btn" data-index="${index}">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="text-content">
                        <p>"${item.text.substring(0, 100)}${item.text.length > 100 ? '...' : ''}"</p>
                    </div>
                    ${audioSection}
                </div>
            `;
        });

        resultDiv.innerHTML = historyHtml;

        // Add event listeners for delete buttons
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-index'));
                deleteHistoryItem(index);
            });
        });

        // Add event listeners for regenerate buttons
        document.querySelectorAll('.regenerate-btn').forEach(btn => {
            btn.addEventListener('click', async function() {
                const index = parseInt(this.getAttribute('data-index'));
                await regenerateAudio(index);
            });
        });
    }

    // Function to regenerate audio for an item
    async function regenerateAudio(index) {
        const item = speechHistory[index];
        if (!item) return;

        // Show loading state
        const speechItem = document.querySelector(`.speech-item[data-index="${index}"]`);
        if (speechItem) {
            const audioSection = speechItem.querySelector('.audio-player');
            if (audioSection) {
                audioSection.innerHTML = `
                    <div class="loading">
                        <i class="fas fa-circle-notch"></i>
                        <span>Regenerating audio, please wait...</span>
                    </div>
                `;
            }
        }

        try {
            const response = await fetch(`/speak?text=${encodeURIComponent(item.text)}&voice=${encodeURIComponent(item.voice)}&speed=${encodeURIComponent(item.speed)}`);

            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);

                // Update the item
                item.audioUrl = url;
                item.needsRegeneration = false;

                // Re-render the history
                renderSpeechHistory();
            } else {
                throw new Error('Failed to regenerate audio');
            }
        } catch (error) {
            console.error('Error regenerating audio:', error);
            // Show error in the audio section
            if (speechItem) {
                const audioSection = speechItem.querySelector('.audio-player');
                if (audioSection) {
                    audioSection.innerHTML = `
                        <div class="error-message">
                            <i class="fas fa-exclamation-triangle"></i>
                            <span>Error regenerating audio: ${error.message}</span>
                        </div>
                    `;
                }
            }
        }
    }

    // Initial rendering of speech history
    renderSpeechHistory();

    // Handle form submission
    document.getElementById('speakForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const text = document.getElementById('text').value;
        const voice = document.getElementById('voice').value;
        const speed = document.getElementById('speed').value;

        // Form validation
        if (!text.trim()) {
            alert('Please enter some text to speak');
            return;
        }

        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `
            <div class="card">
                <div class="loading">
                    <i class="fas fa-circle-notch"></i>
                    <span>Generating audio, please wait...</span>
                </div>
            </div>
        `;

        try {
            const response = await fetch(`/speak?text=${encodeURIComponent(text)}&voice=${voice}&speed=${speed}`);

            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);

                // Add to history (prepend for newest first)
                speechHistory.unshift({
                    text: text,
                    voice: voice,
                    speed: speed,
                    audioUrl: url,
                    timestamp: new Date().toISOString(),
                    needsRegeneration: false
                });

                // Limit history to last 10 items
                if (speechHistory.length > 10) {
                    speechHistory = speechHistory.slice(0, 10);
                }

                // Save to localStorage
                saveToLocalStorage();

                // Render updated history
                renderSpeechHistory();

                // Reset the text field for new input
                document.getElementById('text').value = '';
            } else {
                const error = await response.json();
                resultDiv.innerHTML = `
                    <div class="card">
                        <div class="error-message">
                            <i class="fas fa-exclamation-triangle"></i>
                            <span>Error: ${error.error}</span>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            resultDiv.innerHTML = `
                <div class="card">
                    <div class="error-message">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span>Error: ${error.message}</span>
                    </div>
                </div>
            `;
        }
    });
});
