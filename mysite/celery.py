import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('my_celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'beat-every-day': {
#         'task': 'common.tasks.clean_admin_logs',
#         'schedule': 30.0,
#         'args': (16, 16)
#     }
# }

# app.conf.timezone = 'UTC'
