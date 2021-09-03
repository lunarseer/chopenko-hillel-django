from django.utils import timezone

from celery import shared_task
from .models import LogRecord

from datetime import timedelta


@shared_task
def clean_admin_logs():
    timetodel = timezone.now() - timedelta(days=7)
    print('Cleaning admin logs older than {} ...'.format(timetodel))
    logs = LogRecord.objects.filter(created__lte=timetodel,
                                    path__contains='admin')
    print('{} admin logs deleted'.format(len(logs)))
    logs.delete()
