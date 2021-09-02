from django.utils import timezone
import pytz

from celery import shared_task
from .models import LogRecord



from datetime import timedelta

@shared_task
def clean_admin_logs():
    timetodel = timezone.now() - timedelta(seconds=60)
    print('Cleaning admin logs older than {} ...'.format(timezone.now()))
    print(timetodel)
    logs = LogRecord.objects.filter(created__lte=timetodel,
                                    path__contains='admin')
    print('{} admin logs deleted'.format(len(logs)))
    logs.delete()
    