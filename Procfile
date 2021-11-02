web: gunicorn mysite.wsgi --log-file -
worker: celery -A mysite worker --beat --concurrency 10 -l info