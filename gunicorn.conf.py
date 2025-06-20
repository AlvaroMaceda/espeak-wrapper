"""Gunicorn configuration file for eSpeak Wrapper"""

import os
import multiprocessing

# Bind to 0.0.0.0:5000 by default
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:5000")

# Use auto for worker count (2 * number of CPUs + 1)
workers = int(os.getenv("GUNICORN_WORKERS", (multiprocessing.cpu_count() * 2) + 1))

# Set timeout to 60 seconds
timeout = int(os.getenv("GUNICORN_TIMEOUT", 60))

# Set keepalive to 5 seconds
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", 5))

# Use gevent worker class for better performance with async I/O
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "sync")

# Set access log format
accesslog = os.getenv("GUNICORN_ACCESS_LOG", "-")

# Set error log
errorlog = os.getenv("GUNICORN_ERROR_LOG", "-")

# Log level
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

# Preload application for better performance
preload_app = os.getenv("GUNICORN_PRELOAD_APP", "True").lower() in ["true", "1", "t"]
