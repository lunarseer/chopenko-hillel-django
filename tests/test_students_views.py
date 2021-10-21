import pytest
import re

from django.contrib.messages import get_messages
from django.core.management import call_command

from common.management.commands.utils import random_phone_number
from students.models import Student


@pytest.fixture
@pytest.mark.django_db
def prepare_students():
    call_command('generate_students', count=20)


@pytest.mark.django_db
def test_students_view(client, prepare_students):
    response = client.get('/students_list/')
    assert response.status_code == 200
    content = response.content.decode()
    assert Student.objects.count() != 0
    for student in Student.objects.all():
        assert re.search(f'{student.firstname} {student.lastname}', content)
        assert re.search(student.phone, content)
        assert re.search(f'href="/edit_student/{student.id}"', content)
        assert re.search(f'href="/delete_student/{student.id}"', content)


def test_add_student_form_get(client):
    response = client.get('/add_student/')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search('Add Student to DB', content)
    assert re.search('<label for="id_firstname">First Name:</label>', content)
    assert re.search('<label for="id_lastname">Last Name:</label>', content)
    assert re.search('<label for="id_age">Age:</label>', content)
    assert re.search('<label for="id_phone">Phone:</label>', content)
    assert re.search('type="submit" value="Submit">', content)


@pytest.mark.django_db
def test_add_student_form_post(client):
    studentdata = {'firstname': 'Steven',
                   'lastname': 'King',
                   'age': 25,
                   'phone': random_phone_number()
                   }
    response = client.post('/add_student/', data=studentdata)
    assert response.status_code == 302
    student = Student.objects.first()
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search(f'Student {student.firstname} {student.lastname} Added',
                     message)


@pytest.mark.django_db
def test_edit_student_form_get(client, prepare_students):
    student = Student.objects.first()
    response = client.get(f'/edit_student/{student.id}')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search(student.firstname, content)
    assert re.search(student.lastname, content)
    assert re.search(str(student.age), content)
    assert re.search(student.phone, content)


@pytest.mark.django_db
def test_edit_student_form_post(client, prepare_students):
    student = Student.objects.first()
    studentdata = {'firstname': 'Steven',
                   'lastname': 'King',
                   'age': 25,
                   'phone': random_phone_number()
                   }
    response = client.post(f'/edit_student/{student.id}', data=studentdata)
    assert response.status_code == 302
    editedstudent = Student.objects.get(pk=student.id)
    assert editedstudent.phone == studentdata['phone']
    assert editedstudent.firstname == studentdata['firstname']
    assert editedstudent.lastname == studentdata['lastname']
    assert editedstudent.age == studentdata['age']
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search('Student {} {} saved'.format(editedstudent.firstname,
                                                  editedstudent.lastname),
                     message)


@pytest.mark.django_db
def test_delete_student_form_get(client, prepare_students):
    student = Student.objects.first()
    response = client.get(f'/delete_student/{student.id}')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search(f'Delete Student {student.firstname} {student.lastname}?',
                     content)
    assert re.search('type="submit" name="btn" value="yes"', content)
    assert re.search('type="submit" name="btn" value="no"', content)


@pytest.mark.django_db
def test_delete_student_form_post(client, prepare_students):
    student = Student.objects.first()
    response = client.post(f'/delete_student/{student.id}',
                           data={"btn": "yes"})
    assert response.status_code == 302
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search(f'Student {student.firstname} {student.lastname} Deleted',
                     message)
    assert not Student.objects.filter(firstname=student.firstname,
                                      lastname=student.lastname)
