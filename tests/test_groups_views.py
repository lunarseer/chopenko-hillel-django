import pytest
import re

from django.contrib.messages import get_messages
from django.core.management import call_command


from common.management.commands.utils import random_phone_number
from teachers.models import Teacher
from groups.models import Group


@pytest.fixture
@pytest.mark.django_db
def prepare_students():
    call_command('generate_students', count=20)


@pytest.fixture
@pytest.mark.django_db
def prepare_teachers(prepare_students):
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


@pytest.fixture
@pytest.mark.django_db
def prepare_groups(prepare_teachers):
    call_command('generate_groups', count=Teacher.objects.count())


@pytest.mark.django_db
def test_groups_view(client, prepare_groups):
    response = client.get('/groups_list/')
    assert response.status_code == 200
    content = response.content.decode()
    assert Group.objects.count() != 0
    for group in Group.objects.all():
        assert re.search(f'{group.name}', content)
        assert re.search(f'href="/edit_teacher/{group.teacher.id}', content)
        assert re.search(f'href="/edit_student/{group.headman.id}', content)
        assert re.search(f'href="/edit_group/{group.id}"', content)
        assert re.search(f'href="/delete_group/{group.id}"', content)


def test_add_group_form_get(client):
    response = client.get('/add_group/')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search('Add Group to DB', content)
    assert re.search('<label for="id_name">Name:</label>', content)
    assert re.search('<label for="id_discipline">Discipline:</label>', content)
    assert re.search('type="submit" value="Submit">', content)


@pytest.mark.django_db
def test_add_group_form_post(client, prepare_teachers):
    teacher = Teacher.objects.first()
    groupname = f'01_{teacher.disciplines}'
    groupdata = {'name': f'{teacher.fullname} Group',
                 'discipline': groupname,
                 }
    response = client.post('/add_group/', data=groupdata)
    assert response.status_code == 302
    group = Group.objects.first()
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search(f'Group {group.name} Added',
                     message)


@pytest.mark.django_db
def test_edit_group_form_get(client, prepare_groups):
    group = Group.objects.first()
    response = client.get(f'/edit_group/{group.id}')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search(group.name, content)
    assert re.search(group.discipline, content)
    assert re.search('type="submit" value="Submit">', content)


@pytest.mark.django_db
def test_edit_group_form_post(client, prepare_groups):
    group = Group.objects.first()
    groupdata = {'name': 'Renamed Group',
                 'discipline': 'Renamed Discipline'
                 }
    response = client.post(f'/edit_group/{group.id}', data=groupdata)
    assert response.status_code == 302
    editedgroup = Group.objects.get(pk=group.id)
    assert editedgroup.name == groupdata['name']
    assert editedgroup.discipline == groupdata['discipline']
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search(f'Group {editedgroup.name} saved',
                     message)


@pytest.mark.django_db
def test_delete_group_form_get(client, prepare_groups):
    group = Group.objects.first()
    response = client.get(f'/delete_group/{group.id}')
    assert response.status_code == 200
    content = response.content.decode()
    assert re.search(f'Delete Group {group.name}?',
                     content)
    assert re.search('type="submit" name="btn" value="yes"', content)
    assert re.search('type="submit" name="btn" value="no"', content)


@pytest.mark.django_db
def test_delete_group_form_post(client, prepare_groups):
    group = Group.objects.first()
    response = client.post(f'/delete_group/{group.id}',
                           data={"btn": "yes"})
    assert response.status_code == 302
    message = [m.message for m in get_messages(response.wsgi_request)].pop()
    assert re.search(f'Group {group.name} Deleted',
                     message)
    assert not Group.objects.filter(name=group.name)
