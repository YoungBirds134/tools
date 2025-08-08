import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 10000
max_requests_jitter = 1000
preload_app = True
timeout = 120
keepalive = 60

# Worker temporary directory
worker_tmp_dir = "/tmp"

# Logging
loglevel = os.getenv("LOG_LEVEL", "info").lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "fc_trading_api"

# Server mechanics
daemon = False
user = 1000
group = 1000

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Application
wsgi_file = "app.main:app"
module = "app.main:app"

# Performance - use /tmp for macOS compatibility instead of /dev/shm
worker_tmp_dir = "/tmp"
