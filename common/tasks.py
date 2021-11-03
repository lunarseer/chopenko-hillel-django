
from os import getenv
from dotenv import load_dotenv
from datetime import timedelta
from celery import shared_task

from django.utils import timezone
from django.core.mail import send_mail
from django.core.management import call_command

from .models import LogRecord


load_dotenv()


@shared_task
def clean_admin_logs():
    log_lifetime = int(getenv('ADMIN_LOG_ROTATION_DAYS', 7))
    timetodel = timezone.now() - timedelta(days=log_lifetime)
    print('Cleaning admin logs older than {} ...'.format(timetodel))
    logs = LogRecord.objects.filter(created__lte=timetodel,
                                    path__contains='admin')
    print('{} admin logs deleted'.format(len(logs)))
    logs.delete()


@shared_task
def store_currencies():
    call_command('get_currencies')


@shared_task
def send_mail_message(send_to: list = None,
                      message: str = None,
                      send_from: str = None,
                      subject: str = None):
    send_mail(f'{send_from}:{subject}', message, send_from, send_to)

