#!/bin/bash

if docker ps | grep -q rabbitmq
then 
    echo "Running!"
else
    echo "Not running!"
    docker run -d -p 5672:5672 rabbitmq
fi

celery -A mysite worker -l info & celery -A mysite beat -l info