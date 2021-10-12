import pytest
import django

from django.test import Client

from common.middleware import AdminLogMiddleware
from common.models import LogRecord


@pytest.mark.django_db
def test_adminlog_middleware():
    assert LogRecord.objects.count() == 0
    client = Client()
    client.get('/admin/')
    assert LogRecord.objects.count() == 1