import pytest
import django

django.setup()

# from django.urls import reverse, resolve

from common.middleware import AdminLogMiddleware

def test_middleware():
    assert True