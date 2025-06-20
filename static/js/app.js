// Main JavaScript for eSpeak Wrapper

document.addEventListener('DOMContentLoaded', function() {
    // Store history of speech items
    let speechHistory = [];

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
        let historyHtml = '';
        speechHistory.forEach((item, index) => {
            historyHtml += `
                <div class="card speech-item">
                    <h3 class="result-title">Generated Speech #${speechHistory.length - index}</h3>
                    <div class="text-content">
                        <p><strong>Text:</strong> "${item.text.substring(0, 100)}${item.text.length > 100 ? '...' : ''}"</p>
                    </div>
                    <div class="audio-player">
                        <audio controls ${index === 0 ? 'autoplay' : ''}>
                            <source src="${item.audioUrl}" type="audio/wav">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                    <a href="${item.audioUrl}" download="speech_${Date.now()}.wav" class="download-link">
                        <i class="fas fa-download"></i> Download audio file
                    </a>
                </div>
            `;
        });

        resultDiv.innerHTML = historyHtml;
    }

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
                    timestamp: new Date()
                });

                // Limit history to last 5 items
                if (speechHistory.length > 5) {
                    speechHistory = speechHistory.slice(0, 5);
                }

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
