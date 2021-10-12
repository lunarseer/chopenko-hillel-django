import pytest
import re

from django.test import Client
from django.forms.models import model_to_dict


def test_homepage_endpoint():
    client = Client()
    responce = client.get("")
    assert responce.status_code == 200
    assert re.search('I.Chopenko Student Django Project', responce.content.decode())

def test_fake_generator_endpoint():
    client = Client()
    responce = client.get("/fake_generator/")
    assert responce.status_code == 200
    content = responce.content.decode()
    assert re.search('Performs using Faker python library', content)
    assert re.search('href="/generate_students/"', content)
    assert re.search('href="/generate_teachers/"', content)
    assert re.search('href="/generate_groups/"', content)


def test_fake_generator_entity_endpoint():
    client = Client()
    endpoints = ["/generate_students/",
                 "/generate_teachers/",
                 "/generate_groups/"]
    for endpoint in endpoints:
        responce = client.get(endpoint)
        assert responce.status_code == 200
        content = responce.content.decode()
        assert re.search('<div class="card-header mb-3">Generate Fake', content)
        assert re.search('<input type="submit" value="Generate" align="right">', content)


def test_contact_us_endpoint():
    client = Client()
    responce = client.get('/contact_us/')
    assert responce.status_code == 200
    content = responce.content.decode()
    assert re.search('Contact Us', content)
    assert re.search('<button class="btn btn-primary btn-sm" type="submit">Send Mail</button>', content)
