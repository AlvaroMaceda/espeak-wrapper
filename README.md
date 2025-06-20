# eSpeak Wrapper

A simple Flask web application that provides an API wrapper for the eSpeak text-to-speech synthesizer. The application is served using Gunicorn, a production-grade WSGI server, for better performance and reliability.

## Features

- REST API endpoint for text-to-speech conversion
- Support for various languages and voices through eSpeak

## Requirements

- Python 3.6+
- Flask
- Gunicorn (for production deployment)
- eSpeak (system dependency)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/espeak-wrapper.git
   cd espeak-wrapper
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Make sure eSpeak is installed on your system:
   ```
   # For Ubuntu/Debian
   sudo apt-get install espeak

   # For Fedora
   sudo dnf install espeak

   # For Arch Linux
   sudo pacman -S espeak
   ```

## Usage

### Running Locally

1. Start the Flask development server:
   ```
   python app.py
   ```

1. Or start with Gunicorn (recommended for production):
   ```
   gunicorn --config gunicorn.conf.py app:app
   ```

2. Use the API endpoint:
   ```
   curl "http://127.0.0.1:5000/speak?text=Hello%20world&voice=en"
   ```

### Running with Docker

1. Build the Docker image:
   ```
   docker build -t espeak-wrapper .
   ```

2. Run the container:
   ```
   docker run -p 5000:5000 espeak-wrapper
   ```

3. Use the API endpoint:
   ```
   curl "http://127.0.0.1:5000/speak?text=Hello%20world&voice=en"
   ```

4. Stop the container (press Ctrl+C if running in the foreground, or use docker stop if running detached)
   ```
   # If running detached with -d flag
   docker stop <container_id>
   ```

5. For production deployments, you can run the container in detached mode with restart policy:
   ```
   docker run -d --restart unless-stopped -p 5000:5000 --name espeak-api espeak-wrapper
   ```

### Docker Environment Variables

You can customize the eSpeak wrapper behavior by passing environment variables to the Docker container:

```
docker run -p 5000:5000 \
  -e HOST=0.0.0.0 \
  -e PORT=5000 \
  -e DEFAULT_VOICE=en-us \
  -e DEFAULT_SPEED=150 \
  -e MAX_TEXT_LENGTH=500 \
  -e GUNICORN_WORKERS=2 \
  -e GUNICORN_TIMEOUT=60 \
  espeak-wrapper
```

Available environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| HOST | Host interface to bind | 0.0.0.0 |
| PORT | Port to listen on | 5000 |
| DEFAULT_VOICE | Default voice if not specified | en |
| DEFAULT_SPEED | Default speed if not specified | 160 |
| MAX_TEXT_LENGTH | Maximum allowed text length | No limit |
| GUNICORN_WORKERS | Number of worker processes | 2*CPU+1 |
| GUNICORN_TIMEOUT | Worker timeout in seconds | 60 |
| GUNICORN_LOG_LEVEL | Log level (debug, info, warning, error) | info |

### Docker Volumes

If you need to persist data or mount custom configurations, you can use Docker volumes:

```
# Mount the current directory to /app in the container for development
docker run -p 5000:5000 -v $(pwd):/app espeak-wrapper

# Mount just specific files if needed
docker run -p 5000:5000 -v $(pwd)/.env:/app/.env espeak-wrapper
```

## Usage

### Web Interface

The application includes a web interface accessible at the root URL:

1. Open your browser and navigate to `http://localhost:5000/`
2. Enter the text you want to convert to speech
3. Select a voice/language and set the speed
4. Click "Generate Speech" to create and play the audio
5. You can download the generated speech as a WAV file

### API Endpoints

#### GET /speak
Converts text to speech using eSpeak.

Parameters:
- `text` (required): The text to convert to speech
- `voice` (optional): The voice/language to use (default: "en")
- `speed` (optional): The speaking rate in words per minute (default: 160)

Example:
```
curl "http://localhost:5000/speak?text=Hello%20world&voice=en&speed=150" -o speech.wav
```

#### GET /health
Returns the health status of the API.

Example response:
```json
{
    "status": "healthy",
    "service": "espeak-wrapper",
    "espeak": {
        "status": "available",
        "version": "espeak 1.48.15 2014-08-22"
    },
    "environment": "production"
}
```

## License

MIT
