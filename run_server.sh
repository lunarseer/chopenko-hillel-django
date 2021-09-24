#!/bin/bash
pip install -r $PWD/requirements.txt

export DJANGO_SUPERUSER_PASSWORD=admin

python $PWD/manage.py makemigrations
python $PWD/manage.py migrate --run-syncdb


python $PWD/manage.py createsuperuser --noinput --user admin --email mail@mail.com

python $PWD/manage.py runserver # & source start_rabbitmq.sh