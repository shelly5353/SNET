import multiprocessing
import os

# Server socket configuration
port = os.getenv('PORT', '10000')
bind = f"0.0.0.0:{port}"
workers = 4  # Fixed number of workers for Render
worker_class = 'sync'
timeout = 120  # Increased timeout
keepalive = 2

# Process naming
proc_name = 'snet'
pythonpath = '.'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# SSL (if needed)
# keyfile = 'ssl/key.pem'
# certfile = 'ssl/cert.pem'

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190 