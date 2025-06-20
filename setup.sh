#!/bin/bash

# Setup script for eSpeak Wrapper

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if eSpeak is installed
if ! command -v espeak &> /dev/null; then
    echo "WARNING: eSpeak is not installed on your system."
    echo "Please install it using your package manager:"
    echo "  For Ubuntu/Debian: sudo apt-get install espeak"
    echo "  For Fedora: sudo dnf install espeak"
    echo "  For Arch Linux: sudo pacman -S espeak"
fi

# Create .env file from example if it doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please review and modify .env file as needed."
fi

echo "Setup complete! Run the application with: source venv/bin/activate && python app.py"
