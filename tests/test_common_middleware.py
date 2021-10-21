import pytest

from django.core.management import call_command
from django.forms.models import model_to_dict

from common.management.commands.utils import random_phone_number
from common.models import LogRecord
from students.models import Student


@pytest.fixture
@pytest.mark.django_db
def student_init():
    call_command('generate_students', count=1)


@pytest.mark.django_db
def test_adminlog_middleware(client):
    assert LogRecord.objects.count() == 0
    responce = client.get('/admin/')
    assert responce.status_code == 302 or responce.status_code == 200
    assert LogRecord.objects.count() == 1


@pytest.mark.django_db
def test_phoneformatter_middleware_on_create_fails(client):
    invalid_data = {'firstname': 'Stepan',
                    'lastname': 'Ololoev',
                    'age': 18,
                    'phone': 3891415
                    }
    responce = client.post('/add_student/', invalid_data)
    assert responce.status_code == 200
    assert Student.objects.count() == 0


@pytest.mark.django_db
def test_phoneformatter_middleware_on_create_success(client):
    valid_data = {'firstname': 'Stepan',
                  'lastname': 'Ololoev',
                  'age': 18,
                  'phone': 380661234567
                  }
    responce = client.post('/add_student/', valid_data)
    print(responce.content.decode())
    assert responce.status_code == 302
    assert Student.objects.count() == 1


@pytest.mark.django_db
def test_phoneformatter_middleware_on_edit_success(client, student_init):
    studdata = model_to_dict(Student.objects.first())
    tempphone = random_phone_number()
    assert len(studdata['phone']) == len(tempphone)
    studdata['phone'] = tempphone
    responce = client.post('/edit_student', studdata)
    assert responce.status_code == 200
    assert Student.objects.count() == 1


@pytest.mark.django_db
def test_phoneformatter_middleware_on_edit_fails(client, student_init):
    studdata = model_to_dict(Student.objects.first())
    studdata['phone'] = random_phone_number()[0:-1]
    responce = client.post('/edit_student', studdata)
    assert responce.status_code == 200
    assert Student.objects.count() == 1
    actual_studdata = model_to_dict(Student.objects.first())
    assert actual_studdata['phone'] != studdata['phone']
