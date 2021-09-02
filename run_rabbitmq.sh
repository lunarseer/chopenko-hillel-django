#!/bin/bash

docker run -d -p 5672:5672 rabbitmq

sleep 5

source constants.sh

celery -A mysite worker -l info