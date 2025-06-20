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

1. Build and start the container:
   ```
   docker-compose up -d
   ```

2. Use the API endpoint:
   ```
   curl "http://127.0.0.1:5000/speak?text=Hello%20world&voice=en"
   ```

3. Stop the container:
   ```
   docker-compose down
   ```

### Running with Docker (manual approach)

1. Build the Docker image:
   ```
   docker build -t espeak-wrapper .
   ```

2. Run the container:
   ```
   docker run -p 5000:5000 espeak-wrapper
   ```

## API Endpoints

### GET /speak
Converts text to speech using eSpeak.

Parameters:
- `text` (required): The text to convert to speech
- `voice` (optional): The voice/language to use (default: "en")
- `speed` (optional): The speaking rate in words per minute (default: 160)

## License

MIT
