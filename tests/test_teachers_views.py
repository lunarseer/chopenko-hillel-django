import pytest
import re

from django.contrib.messages import get_messages

from common.management.commands.utils import random_phone_number
from teachers.models import Teacher


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


@pytest.mark.django_db
def test_teachers_view(client, prepare_teachers):
    response = client.get('/teachers_list/')
    assert response.status_code == 200
    content = response.content.decode()
    assert Teacher.objects.count() != 0
    for teacher in Teacher.objects.all():
        assert re.search(f'{teacher.firstname} {teacher.lastname}', content)
        assert re.search(teacher.phone, content)
        assert re.search(f'href="/edit_teacher/{teacher.id}"', content)
        assert re.search(f'href="/delete_teacher/{teacher.id}"', content)


def test_add_teacher_form_get(client):
    response = client.get('/add_teacher/')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search('Add Teacher to DB', content)
    assert re.search('<label for="id_firstname">First Name:</label>', content)
    assert re.search('<label for="id_lastname">Last Name:</label>', content)
    assert re.search('<label for="id_age">Age:</label>', content)
    assert re.search('<label for="id_phone">Phone:</label>', content)
    assert re.search('type="submit" value="Submit">', content)


@pytest.mark.django_db
def test_add_teacher_form_post(client):
    teacherdata = {'firstname': 'Steven',
                   'lastname': 'King',
                   'age': 25,
                   'phone': random_phone_number()
                   }
    response = client.post('/add_teacher/', data=teacherdata)
    assert response.status_code == 302
    teacher = Teacher.objects.first()
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search(f'Teacher {teacher.firstname} {teacher.lastname} Added',
                     message)


@pytest.mark.django_db
def test_edit_teacher_form_get(client, prepare_teachers):
    teacher = Teacher.objects.first()
    response = client.get(f'/edit_teacher/{teacher.id}')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search(teacher.firstname, content)
    assert re.search(teacher.lastname, content)
    assert re.search(str(teacher.age), content)
    assert re.search(teacher.phone, content)


@pytest.mark.django_db
def test_edit_teacher_form_post(client, prepare_teachers):
    teacher = Teacher.objects.first()
    teacherdata = {'firstname': 'Steven',
                   'lastname': 'King',
                   'age': 25,
                   'phone': random_phone_number(),
                   'disciplines': 'Horror'
                   }
    response = client.post(f'/edit_teacher/{teacher.id}', data=teacherdata)
    assert response.status_code == 302
    editedteacher = Teacher.objects.get(pk=teacher.id)
    assert editedteacher.phone == teacherdata['phone']
    assert editedteacher.firstname == teacherdata['firstname']
    assert editedteacher.lastname == teacherdata['lastname']
    assert editedteacher.age == teacherdata['age']
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search('Teacher {} {} saved'.format(editedteacher.firstname,
                                                  editedteacher.lastname),
                     message)


@pytest.mark.django_db
def test_delete_teacher_form_get(client, prepare_teachers):
    teacher = Teacher.objects.first()
    response = client.get(f'/delete_teacher/{teacher.id}')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search(f'Delete Teacher {teacher.firstname} {teacher.lastname}?',
                     content)
    assert re.search('type="submit" name="btn" value="yes"', content)
    assert re.search('type="submit" name="btn" value="no"', content)


@pytest.mark.django_db
def test_delete_teacher_form_post(client, prepare_teachers):
    teacher = Teacher.objects.first()
    response = client.post(f'/delete_teacher/{teacher.id}',
                           data={"btn": "yes"})
    assert response.status_code == 302
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search(f'Teacher {teacher.firstname} {teacher.lastname} Deleted',
                     message)
    assert not Teacher.objects.filter(firstname=teacher.firstname,
                                      lastname=teacher.lastname)
