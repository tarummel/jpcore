wsgi_app = "jpcore.wsgi:application"
loglevel = "warn"
workers = 2
threads = 1
# django defaults to 8000, 8008 as prefered non-default port - needs to match with nginx
bind = "0.0.0.0:8008"
reload = True
accesslog = "/var/log/jpcore/gunicorn.log"
errorlog = "/var/log/jpcore/gunicorn_error.log"
capture_output = True
# /var/run/gunicorn needs www-data ownership
pidfile = "/var/run/gunicorn/gunicorn.pid"
# replaces the need for nohup and & 
daemon = True
