web: python manage.py collectstatic --no-input; gunicorn mysite.wsgi --log-file - --log-level debug
worker: celery -A mysite worker --beat --concurrency 10 -l info