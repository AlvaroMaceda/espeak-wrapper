from flask import Flask, request, send_file, jsonify
import os
import subprocess
import tempfile
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>eSpeak Wrapper</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
            <style>
                :root {
                    --primary-color: #4285f4;
                    --primary-dark: #3367d6;
                    --secondary-color: #34a853;
                    --text-color: #202124;
                    --light-gray: #f8f9fa;
                    --gray: #dadce0;
                    --error: #ea4335;
                }

                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }

                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: var(--text-color);
                    background-color: #ffffff;
                    padding: 0;
                    margin: 0;
                }

                .container {
                    width: 100%;
                    max-width: 1200px;
                    padding: 20px;
                    margin: 0 auto;
                }

                header {
                    background-color: var(--primary-color);
                    color: white;
                    padding: 1rem 0;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }

                .header-content {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }

                h1 {
                    margin: 0;
                    font-size: 1.8rem;
                }

                .tagline {
                    font-size: 1rem;
                    opacity: 0.9;
                }

                main {
                    padding: 2rem 0;
                }

                .card {
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
                    padding: 2rem;
                    margin-bottom: 1.5rem;
                }

                .form-title {
                    margin-bottom: 1.5rem;
                    color: var(--text-color);
                    font-size: 1.5rem;
                }

                .form-group {
                    margin-bottom: 1.5rem;
                }

                label {
                    display: block;
                    margin-bottom: 0.5rem;
                    font-weight: 500;
                }

                textarea {
                    width: 100%;
                    border: 1px solid var(--gray);
                    border-radius: 4px;
                    padding: 0.8rem;
                    font-family: inherit;
                    font-size: 1rem;
                    min-height: 100px;
                    resize: vertical;
                    transition: border 0.3s;
                }

                textarea:focus {
                    outline: none;
                    border-color: var(--primary-color);
                }

                select,
                input[type="number"] {
                    width: 100%;
                    padding: 0.8rem;
                    border: 1px solid var(--gray);
                    border-radius: 4px;
                    font-family: inherit;
                    font-size: 1rem;
                    transition: border 0.3s;
                }

                select:focus,
                input[type="number"]:focus {
                    outline: none;
                    border-color: var(--primary-color);
                }

                @media (min-width: 768px) {
                    .form-row {
                        display: flex;
                        gap: 20px;
                    }

                    .form-group.half {
                        flex: 1;
                    }
                }

                button {
                    background-color: var(--primary-color);
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 0.8rem 1.5rem;
                    font-size: 1rem;
                    font-weight: 500;
                    cursor: pointer;
                    transition: background 0.3s;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                }

                button:hover {
                    background-color: var(--primary-dark);
                }

                button i {
                    margin-right: 8px;
                }

                .result {
                    padding: 1rem 0;
                }

                .result-title {
                    margin-bottom: 1rem;
                    color: var(--text-color);
                    font-size: 1.3rem;
                }

                .audio-player {
                    width: 100%;
                    padding: 1rem;
                    background-color: var(--light-gray);
                    border-radius: 8px;
                    margin-bottom: 1rem;
                }

                audio {
                    width: 100%;
                }

                .download-link {
                    display: inline-flex;
                    align-items: center;
                    text-decoration: none;
                    color: var(--primary-color);
                    font-weight: 500;
                    margin-top: 0.5rem;
                }

                .download-link i {
                    margin-right: 8px;
                }

                .loading {
                    display: flex;
                    align-items: center;
                    color: var(--primary-color);
                }

                .loading i {
                    margin-right: 8px;
                    animation: spin 1s linear infinite;
                }

                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }

                .error-message {
                    color: var(--error);
                    padding: 0.5rem 0;
                }

                footer {
                    background-color: var(--light-gray);
                    padding: 1rem 0;
                    text-align: center;
                    color: #70757a;
                    font-size: 0.9rem;
                    margin-top: 2rem;
                }
            </style>
        </head>
        <body>
            <header>
                <div class="container header-content">
                    <div>
                        <h1>eSpeak Wrapper</h1>
                        <p class="tagline">Text-to-speech conversion API</p>
                    </div>
                    <div>
                        <a href="/api" style="color: white; text-decoration: none;">
                            <i class="fas fa-book"></i> API Docs
                        </a>
                    </div>
                </div>
            </header>

            <main class="container">
                <div class="card">
                    <h2 class="form-title">Convert Text to Speech</h2>

                    <form id="speakForm">
                        <div class="form-group">
                            <label for="text">Text to speak</label>
                            <textarea id="text" name="text" required placeholder="Enter your text here..."></textarea>
                        </div>

                        <div class="form-row">
                            <div class="form-group half">
                                <label for="voice">Voice/Language</label>
                                <select id="voice" name="voice">
                                    <option value="en">English</option>
                                    <option value="en-us">English (US)</option>
                                    <option value="en-gb">English (UK)</option>
                                    <option value="es">Spanish</option>
                                    <option value="es-la">Spanish (Latin America)</option>
                                    <option value="fr">French</option>
                                    <option value="de">German</option>
                                    <option value="it">Italian</option>
                                    <option value="pt">Portuguese</option>
                                    <option value="pt-br">Portuguese (Brazil)</option>
                                    <option value="ru">Russian</option>
                                    <option value="zh">Chinese</option>
                                    <option value="ja">Japanese</option>
                                    <option value="ko">Korean</option>
                                    <option value="hi">Hindi</option>
                                    <option value="ar">Arabic</option>
                                </select>
                            </div>

                            <div class="form-group half">
                                <label for="speed">Speed (words per minute)</label>
                                <input type="number" id="speed" name="speed" value="160" min="80" max="500">
                            </div>
                        </div>

                        <button type="submit"><i class="fas fa-play"></i> Generate Speech</button>
                    </form>
                </div>

                <div class="result" id="result"></div>
            </main>

            <footer>
                <div class="container">
                    <p>&copy; 2025 eSpeak Wrapper - A simple API for text-to-speech conversion</p>
                </div>
            </footer>

            <script>
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
            </script>
        </body>
    </html>
    '''

@app.route('/speak')
def speak():
    text = request.args.get('text')
    default_voice = os.getenv('DEFAULT_VOICE', 'en')
    default_speed = os.getenv('DEFAULT_SPEED', '160')
    voice = request.args.get('voice', default_voice)
    speed = request.args.get('speed', default_speed)

    if not text:
        return jsonify({"error": "Text parameter is required"}), 400

    # Check text length if MAX_TEXT_LENGTH is defined
    max_length = os.getenv('MAX_TEXT_LENGTH')
    if max_length and len(text) > int(max_length):
        return jsonify({"error": f"Text exceeds maximum length of {max_length} characters"}), 400

    try:
        # Create a temporary file for the audio output
        output_file = os.path.join(tempfile.gettempdir(), f"espeak_{uuid.uuid4()}.wav")

        # Run espeak command
        espeak_path = os.getenv('ESPEAK_PATH', 'espeak')
        command = [
            espeak_path,
            '-v', voice,
            '-s', speed,
            '-w', output_file,
            text
        ]

        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode != 0:
            return jsonify({"error": f"eSpeak error: {process.stderr}"}), 500

        # Send the generated audio file
        return send_file(output_file, mimetype='audio/wav', as_attachment=False)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temporary file if it exists
        if 'output_file' in locals() and os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass

@app.route('/health')
def health():
    # Check if espeak is available
    try:
        process = subprocess.run(['espeak', '--version'], capture_output=True, text=True)
        espeak_status = "available" if process.returncode == 0 else "unavailable"
        espeak_version = process.stdout.strip() if process.returncode == 0 else "unknown"
    except Exception:
        espeak_status = "unavailable"
        espeak_version = "unknown"

    # Get application information
    app_info = {
        "status": "healthy",
        "service": "espeak-wrapper",
        "espeak": {
            "status": espeak_status,
            "version": espeak_version
        },
        "environment": os.getenv('FLASK_ENV', 'production')
    }

    return jsonify(app_info), 200

@app.route('/api')
def api_docs():
    return '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>eSpeak Wrapper API Documentation</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
            <style>
                :root {
                    --primary-color: #4285f4;
                    --primary-dark: #3367d6;
                    --secondary-color: #34a853;
                    --text-color: #202124;
                    --light-gray: #f8f9fa;
                    --gray: #dadce0;
                    --code-bg: #f6f8fa;
                }

                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }

                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: var(--text-color);
                    background-color: #ffffff;
                    padding: 0;
                    margin: 0;
                }

                .container {
                    width: 100%;
                    max-width: 1200px;
                    padding: 20px;
                    margin: 0 auto;
                }

                header {
                    background-color: var(--primary-color);
                    color: white;
                    padding: 1rem 0;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }

                .header-content {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }

                h1 {
                    margin: 0;
                    font-size: 1.8rem;
                }

                .tagline {
                    font-size: 1rem;
                    opacity: 0.9;
                }

                main {
                    padding: 2rem 0;
                }

                .card {
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
                    padding: 2rem;
                    margin-bottom: 1.5rem;
                }

                .section-title {
                    margin-bottom: 1rem;
                    color: var(--text-color);
                    font-size: 1.5rem;
                    padding-bottom: 0.5rem;
                    border-bottom: 1px solid var(--gray);
                }

                .endpoint {
                    margin-bottom: 2rem;
                }

                .endpoint-title {
                    display: flex;
                    align-items: center;
                    margin-bottom: 1rem;
                }

                .method {
                    background-color: var(--primary-color);
                    color: white;
                    padding: 0.2rem 0.5rem;
                    border-radius: 4px;
                    font-size: 0.8rem;
                    margin-right: 0.5rem;
                }

                .url {
                    font-family: monospace;
                    font-weight: bold;
                }

                .description {
                    margin-bottom: 1rem;
                }

                .params-title {
                    font-weight: bold;
                    margin-bottom: 0.5rem;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 1rem;
                }

                th, td {
                    text-align: left;
                    padding: 0.75rem;
                    border-bottom: 1px solid var(--gray);
                }

                th {
                    background-color: var(--light-gray);
                }

                .code-example {
                    background-color: var(--code-bg);
                    padding: 1rem;
                    border-radius: 4px;
                    font-family: monospace;
                    overflow-x: auto;
                    margin-bottom: 1rem;
                }

                .example-title {
                    font-weight: bold;
                    margin-bottom: 0.5rem;
                }

                .back-link {
                    display: inline-block;
                    margin-top: 1rem;
                    color: var(--primary-color);
                    text-decoration: none;
                }

                .back-link i {
                    margin-right: 0.5rem;
                }

                footer {
                    background-color: var(--light-gray);
                    padding: 1rem 0;
                    text-align: center;
                    color: #70757a;
                    font-size: 0.9rem;
                    margin-top: 2rem;
                }

                @media (max-width: 768px) {
                    .card {
                        padding: 1.5rem;
                    }

                    .endpoint-title {
                        flex-direction: column;
                        align-items: flex-start;
                    }

                    .method {
                        margin-bottom: 0.5rem;
                    }

                    th, td {
                        padding: 0.5rem;
                    }
                }
            </style>
        </head>
        <body>
            <header>
                <div class="container header-content">
                    <div>
                        <h1>eSpeak Wrapper API</h1>
                        <p class="tagline">Documentation</p>
                    </div>
                </div>
            </header>

            <main class="container">
                <div class="card">
                    <h2 class="section-title">API Overview</h2>
                    <p>The eSpeak Wrapper API provides a simple way to convert text to speech using the eSpeak text-to-speech synthesizer.</p>
                </div>

                <div class="card">
                    <h2 class="section-title">Endpoints</h2>

                    <div class="endpoint">
                        <div class="endpoint-title">
                            <span class="method">GET</span>
                            <span class="url">/speak</span>
                        </div>
                        <p class="description">Converts text to speech and returns an audio file.</p>

                        <h4 class="params-title">Query Parameters</h4>
                        <table>
                            <thead>
                                <tr>
                                    <th>Parameter</th>
                                    <th>Type</th>
                                    <th>Required</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>text</td>
                                    <td>string</td>
                                    <td>Yes</td>
                                    <td>The text to convert to speech</td>
                                </tr>
                                <tr>
                                    <td>voice</td>
                                    <td>string</td>
                                    <td>No</td>
                                    <td>The voice/language to use (default: "en")</td>
                                </tr>
                                <tr>
                                    <td>speed</td>
                                    <td>integer</td>
                                    <td>No</td>
                                    <td>The speaking rate in words per minute (default: 160)</td>
                                </tr>
                            </tbody>
                        </table>

                        <h4 class="example-title">Example Request:</h4>
                        <div class="code-example">
                            GET /speak?text=Hello%20world&voice=en&speed=160
                        </div>

                        <h4 class="example-title">Response:</h4>
                        <p>Returns a WAV audio file with the synthesized speech.</p>
                        <p>Content-Type: audio/wav</p>
                    </div>

                    <div class="endpoint">
                        <div class="endpoint-title">
                            <span class="method">GET</span>
                            <span class="url">/health</span>
                        </div>
                        <p class="description">Returns the health status of the API.</p>

                        <h4 class="example-title">Example Response:</h4>
                        <div class="code-example">
{
    "status": "healthy",
    "service": "espeak-wrapper",
    "espeak": {
        "status": "available",
        "version": "espeak 1.48.15 2014-08-22"
    },
    "environment": "production"
}
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h2 class="section-title">Code Examples</h2>

                    <h4 class="example-title">cURL:</h4>
                    <div class="code-example">
curl "http://localhost:5000/speak?text=Hello%20world&voice=en" -o speech.wav
                    </div>

                    <h4 class="example-title">JavaScript:</h4>
                    <div class="code-example">
fetch('http://localhost:5000/speak?text=Hello%20world&voice=en')
  .then(response => response.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.play();
  })
  .catch(error => console.error('Error:', error));
                    </div>

                    <h4 class="example-title">Python:</h4>
                    <div class="code-example">
import requests

response = requests.get(
    'http://localhost:5000/speak',
    params={'text': 'Hello world', 'voice': 'en'},
    stream=True
)

if response.status_code == 200:
    with open('speech.wav', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print('Audio file saved as speech.wav')
else:
    print(f'Error: {response.json().get("error")}')
                    </div>
                </div>

                <a href="/" class="back-link"><i class="fas fa-arrow-left"></i> Back to Web Interface</a>
            </main>

            <footer>
                <div class="container">
                    <p>&copy; 2025 eSpeak Wrapper - A simple API for text-to-speech conversion</p>
                </div>
            </footer>
        </body>
    </html>
    '''

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']

    app.run(host=host, port=port, debug=debug)
