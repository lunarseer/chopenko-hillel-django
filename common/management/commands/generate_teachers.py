from random import randrange
from .utils import (get_random_entity,
                    random_phone_number,
                    get_random_objects)

from django.core.management.base import BaseCommand

from faker import Faker

from teachers.models import Teacher
from students.models import Student
from groups.models import Group


class Command(BaseCommand):
    # help = 'Generate numbers of teachers'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', type=int, default=100)

    def do(self, count):
        gen = Faker()
        for _ in range(count):
            teacher = Teacher.objects.create(firstname=gen.first_name(),
                                             lastname=gen.last_name(),
                                             age=randrange(25, 70),
                                             phone=random_phone_number())
            students = get_random_entity(Student, randrange(1, 10))
            headman = get_random_objects(list(students), 1).pop()
            group = Group.objects.create(name=f'{teacher.fullname}_group',
                                         teacher=teacher,
                                         headman=headman)
            group.students.set(students)
            group.save()

    def handle(self, **options):
        count = options.get('count', 0)
        if count:
            try:
                self.do(count)
            except AttributeError:
                msg = 'Teacher requires at least 1 Student exists!'
                raise Exception(msg)
