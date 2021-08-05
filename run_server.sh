#!/bin/bash
#pip install -r $PWD/requirements.txt

source constants.sh

#flake8

#export DJANGO_SUPERUSER_PASSWORD=admin

python $PWD/manage.py makemigrations
python $PWD/manage.py migrate

#python $PWD/manage.py createsuperuser --noinput --user admin --email mail@mail.com

#python $PWD/manage.py generate_teachers 50
#python $PWD/manage.py generate_students 100

python $PWD/manage.py runserver