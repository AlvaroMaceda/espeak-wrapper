from flask import Flask, request, send_file, jsonify, render_template
import os
import subprocess
import tempfile
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']

    app.run(host=host, port=port, debug=debug)
