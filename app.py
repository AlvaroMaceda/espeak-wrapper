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
    <html>
        <head>
            <title>eSpeak Wrapper</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                form { background: #f8f8f8; padding: 20px; border-radius: 5px; }
                textarea { width: 100%; height: 100px; margin-bottom: 10px; }
                select, input { margin-bottom: 10px; padding: 5px; }
                button { background: #4CAF50; color: white; border: none; padding: 10px 15px; cursor: pointer; }
                .result { margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1>eSpeak Wrapper</h1>
            <p>Convert text to speech using the eSpeak synthesizer.</p>

            <form id="speakForm">
                <div>
                    <label for="text">Text to speak:</label>
                    <textarea id="text" name="text" required></textarea>
                </div>

                <div>
                    <label for="voice">Voice/Language:</label>
                    <select id="voice" name="voice">
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                        <option value="it">Italian</option>
                    </select>
                </div>

                <div>
                    <label for="speed">Speed (words per minute):</label>
                    <input type="number" id="speed" name="speed" value="160" min="80" max="500">
                </div>

                <button type="submit">Generate Speech</button>
            </form>

            <div class="result" id="result"></div>

            <script>
                document.getElementById('speakForm').addEventListener('submit', async function(e) {
                    e.preventDefault();

                    const text = document.getElementById('text').value;
                    const voice = document.getElementById('voice').value;
                    const speed = document.getElementById('speed').value;

                    const resultDiv = document.getElementById('result');
                    resultDiv.innerHTML = '<p>Generating audio...</p>';

                    try {
                        const response = await fetch(`/speak?text=${encodeURIComponent(text)}&voice=${voice}&speed=${speed}`);

                        if (response.ok) {
                            const blob = await response.blob();
                            const url = URL.createObjectURL(blob);

                            resultDiv.innerHTML = `
                                <h3>Generated Speech</h3>
                                <audio controls autoplay>
                                    <source src="${url}" type="audio/wav">
                                    Your browser does not support the audio element.
                                </audio>
                                <p><a href="${url}" download="speech.wav">Download audio</a></p>
                            `;
                        } else {
                            const error = await response.json();
                            resultDiv.innerHTML = `<p>Error: ${error.error}</p>`;
                        }
                    } catch (error) {
                        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
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

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']

    app.run(host=host, port=port, debug=debug)
