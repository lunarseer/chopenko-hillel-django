import pytest
import re

from datetime import datetime as dt

from django.core.management import call_command
from django.contrib.messages import get_messages

from common.management.commands.utils import random_phone_number
from common.models import CurrencyStamp
from students.models import Student
from teachers.models import Teacher
from groups.models import Group


@pytest.fixture
@pytest.mark.django_db
def prepare_currencies():
    currencies = []
    stamp = CurrencyStamp(currency='EUR',
                          bank='MINI',
                          exchangerate='30.0',
                          created=dt.now())
    currencies.append(stamp)
    CurrencyStamp.objects.bulk_create(currencies)
    return currencies


@pytest.fixture
@pytest.mark.django_db
def prepare_students():
    call_command('generate_students', count=10)


@pytest.fixture
@pytest.mark.django_db
def prepare_teachers():
    teachers = []
    teacher = Teacher(firstname='Carlos',
                      lastname='Castaneda',
                      age=99,
                      phone=random_phone_number(),
                      disciplines='uncommon expirience')
    teachers.append(teacher)
    teacher = Teacher(firstname='Tiago',
                      lastname='Costa',
                      age=40,
                      phone=random_phone_number(),
                      disciplines='common expirience')
    teachers.append(teacher)
    Teacher.objects.bulk_create(teachers)


def test_homepage_view(client):
    # test GET method
    response = client.get("")
    assert response.status_code == 200
    assert re.search('I.Chopenko Student Django Project',
                     response.content.decode())


@pytest.mark.django_db
def test_currency_view(client, prepare_currencies):
    response = client.get('/currencies/')
    assert response.status_code == 200
    content = response.content.decode()
    for stamp in prepare_currencies:
        created = stamp.created.strftime("%Y-%m-%d %H:%M")
        assert re.search(created, content)
        assert re.search(stamp.currency, content)
        assert re.search(stamp.bank, content)
        assert re.search(stamp.exchangerate, content)


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
    # test GET method
    response = client.get('/contact_us/')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search('Contact Us', content)
    assert re.search('type="submit">Send Mail</button>', content)


@pytest.mark.skip
def test_contact_us_sendmail_success(client):
    """ test POST method
    disabled just because, i'm not sure about celery with pytest
    and was too lazy for check it. xD
    P.S. Hope u lazy enough too for configuring mail. xDD
    """
    data = {'send_from': 'ololoev@test.com',
            'subject': 'hope it works',
            'message': 'Just Stupid Message'
            }
    response = client.post('/contact_us/', data)
    assert response.status_code == 302
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search('Email Sent.', message)


def test_contact_us_sendmail_fails(client):
    # test POST method(case when celery unavailable)
    data = {'send_from': 'ololoev@test.com',
            'subject': 'hope it not works',
            'message': 'Another Stupid Message'
            }
    response = client.post('/contact_us/', data)
    assert response.status_code == 302
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search('Connection refused', message)


def test_generate_students_view(client):
    # test GET method
    get_response = client.get('/generate_students/')
    assert get_response.status_code == 200
    content = get_response.content.decode()
    assert re.search('<div class="card-header mb-3">Generate Fake Students',
                     content)
    assert re.search('<input type="submit" value="Generate" align="right">',
                     content)


@pytest.mark.django_db
def test_generate_students(client):
    # test POST method
    endpoint, count = '/generate_students/', 10
    response = client.post(endpoint, data={"count": count})
    assert response.status_code == 302
    assert Student.objects.count() == count
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search('Students Generated.', message)


def test_generate_teachers_view(client):
    # test GET method
    response = client.get('/generate_teachers/')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search('<div class="card-header mb-3">Generate Fake Teachers',
                     content)
    assert re.search('<input type="submit" value="Generate" align="right">',
                     content)


@pytest.mark.django_db
def test_generate_teachers(client, prepare_students):
    # test POST method
    endpoint, count = '/generate_teachers/', 2
    response = client.post(endpoint, data={"count": count})
    assert response.status_code == 302
    assert Student.objects.count() == 10    # Set in the fixture
    assert Teacher.objects.count() == count
    assert Group.objects.count() == count
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search('Teachers Generated.', message)


def test_generate_groups_view(client):
    # test GET method
    response = client.get('/generate_groups/')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search('<div class="card-header mb-3">Generate Fake Groups',
                     content)
    assert re.search('<input type="submit" value="Generate" align="right">',
                     content)


@pytest.mark.django_db
def test_generate_groups(client, prepare_students, prepare_teachers):
    # test POST method
    endpoint, count = '/generate_groups/', 2
    response = client.post(endpoint, data={"count": count})
    assert response.status_code == 302
    assert Student.objects.count() == 10    # Set in the fixture
    assert Teacher.objects.count() == count
    assert Group.objects.count() == count
    groups = Group.objects.all()
    for group in groups:
        assert group.teacher in Teacher.objects.all()
        students = group.students.all()
        for student in students:
            assert student in Student.objects.all()
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search('Groups Generated.', message)
