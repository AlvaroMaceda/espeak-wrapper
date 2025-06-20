#!/bin/bash

# Run script for eSpeak Wrapper with Gunicorn

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn not found. Installing..."
    pip install gunicorn
fi

# Run with Gunicorn
echo "Starting eSpeak Wrapper with Gunicorn..."
gunicorn --config gunicorn.conf.py app:app
