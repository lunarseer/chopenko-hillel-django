# IT-HILLEL Django Project (I.Chopenko)

USAGE

- create and activate virtualenv

- rename example.env to .env and properly configure it, if needed    
(For this homework, DEBUG set to False, due to django Http error handling)
   
- start run_server.sh in root folder (Rabbit-MQ starting using docker container)
(For this homework, RabbitMQ and Celery disabled)

- Enjoy, Homepage on http://127.0.0.1:8000

DJANGO MANAGEMENT COMMANDS

- run './manage.py get_currencies' for saving exchanges stamp to database manually
- run './manage.py generate_students <int>' to generate number of fake students
- run './manage.py generate_teachers <int>' to generate number of fake teachers
- run './manage.py generate_groups <int>' to generate number of fake groups(requires existing students and teachers)

TROUBLESHOOTING

- remove old project and clone again, or remove db.sqlite3