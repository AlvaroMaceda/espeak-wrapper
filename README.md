# eSpeak Wrapper

A simple Flask web application that provides an API wrapper for the eSpeak text-to-speech synthesizer.

## Features

- REST API endpoint for text-to-speech conversion
- Support for various languages and voices through eSpeak

## Requirements

- Python 3.6+
- Flask
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

1. Start the Flask server:
   ```
   python app.py
   ```

2. Use the API endpoint:
   ```
   curl "http://127.0.0.1:5000/speak?text=Hello%20world&voice=en"
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
