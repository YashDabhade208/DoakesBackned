# Gunicorn configuration for production deployment

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restarting
preload_app = True
worker_tmp_dir = "/dev/shm"

# Logging
loglevel = "info"
accesslog = "/app/logs/gunicorn_access.log"
errorlog = "/app/logs/gunicorn_error.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'ai_audio_listener'

# Server mechanics
daemon = False
pidfile = "/app/gunicorn.pid"
user = "app"
group = "app"
tmp_upload_dir = None

# SSL (uncomment if using SSL)
# keyfile = "/etc/ssl/private/ai_audio_listener.key"
# certfile = "/etc/ssl/certs/ai_audio_listener.crt"

# Application
chdir = "/app"
module = "main:app"
