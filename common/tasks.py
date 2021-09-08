from django.utils import timezone
from django.core.mail import send_mail

from celery import shared_task

from .models import LogRecord, MonoCurrency, NbuCurrency

from datetime import timedelta





@shared_task
def clean_admin_logs():
    timetodel = timezone.now() - timedelta(days=7)
    print('Cleaning admin logs older than {} ...'.format(timetodel))
    logs = LogRecord.objects.filter(created__lte=timetodel,
                                    path__contains='admin')
    print('{} admin logs deleted'.format(len(logs)))
    logs.delete()


@shared_task
def store_currencies():
    pass


@shared_task
def send_mail_message(send_to: list = None,
                      message: str = None,
                      send_from: str = None,
                      subject: str = None):
    send_mail(f'{send_from}:{subject}', message, send_from, send_to)
