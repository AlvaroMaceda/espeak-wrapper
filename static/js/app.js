// Main JavaScript for eSpeak Wrapper

document.addEventListener('DOMContentLoaded', function() {
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

                resultDiv.innerHTML = `
                    <div class="card">
                        <h3 class="result-title">Generated Speech</h3>
                        <div class="audio-player">
                            <audio controls autoplay>
                                <source src="${url}" type="audio/wav">
                                Your browser does not support the audio element.
                            </audio>
                        </div>
                        <a href="${url}" download="speech.wav" class="download-link">
                            <i class="fas fa-download"></i> Download audio file
                        </a>
                    </div>
                `;
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
