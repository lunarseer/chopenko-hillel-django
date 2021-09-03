#!/bin/bash

# docker run -d -p 5672:5672 rabbitmq

celery -A mysite worker -l info & celery -A mysite beat -l info