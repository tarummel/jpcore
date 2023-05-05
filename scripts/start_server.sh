# https://docs.gunicorn.org/en/stable/settings.html#access-log-format
gunicorn \
    -w 2 \
    --threads=1 \
    --bind='unix:/run/gunicorn.sock' \
    --access-logfile='/var/log/jpcore/gunicorn.log' \
    --error-logfile='/var/log/jpcore/gunicorn_error.log' \
    --access_log_format='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
    'jpcore.wsgi:application'
