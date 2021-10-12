import pytest
import re

from django.test import Client
from django.urls import reverse
from django.core.management import call_command
from django.contrib.messages import get_messages

from students.models import Student
from teachers.models import Teacher
from groups.models import Group


@pytest.fixture
def client():
    return Client()

@pytest.fixture
@pytest.mark.django_db
def generate_students():
    call_command('generate_students', count=10)


def test_homepage_view(client):
    # test GET method
    response = client.get("")
    assert response.status_code == 200
    assert re.search('I.Chopenko Student Django Project',
                     response.content.decode())


def test_fake_generator_view(client):
    # test GET method
    response = client.get("/fake_generator/")
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search('Performs using Faker python library', content)
    assert re.search('href="/generate_students/"', content)
    assert re.search('href="/generate_teachers/"', content)
    assert re.search('href="/generate_groups/"', content)


def test_contact_us_endpoint(client):
    endpoint = '/contact_us/'
    # test GET method
    response = client.get(endpoint)
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search('Contact Us', content)
    assert re.search('<button class="btn btn-primary btn-sm" type="submit">Send Mail</button>', content)
    # test POST method
    data = {'send_from': 'ololoev@test.com',
            'subject': 'hope it works',
            'message': 'Just Random Message'
            }
    response = client.post(endpoint, data)
    assert response.status_code == 302
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search('Connection refused', message) 


@pytest.mark.django_db
def test_generate_students(client):
    endpoint, count = '/generate_students/', 10
    # test GET method
    get_response = client.get(endpoint)
    assert get_response.status_code == 200
    content = get_response.content.decode()
    assert re.search('<div class="card-header mb-3">Generate Fake Students',
                     content)
    assert re.search('<input type="submit" value="Generate" align="right">',
                     content)
    # test POST method
    assert Student.objects.count() == 0
    post_response = client.post(endpoint, data={"count": count})
    assert post_response.status_code == 302
    assert Student.objects.count() == count
    message = [m.message for m in get_messages(post_response.wsgi_request)].pop()
    assert re.search('Students Generated.', message) 


@pytest.mark.django_db
def test_generate_teachers(client, generate_students):
    endpoint, count = '/generate_teachers/', 2
    # test GET method
    response = client.get(endpoint)
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search('<div class="card-header mb-3">Generate Fake Teachers',
                     content)
    assert re.search('<input type="submit" value="Generate" align="right">',
                     content)
    # test POST method
    response = client.post(endpoint, data={"count": count})
    assert Student.objects.count() == 10
    assert Teacher.objects.count() == count
    assert Group.objects.count() == count
