from random import randrange

from .utils import (get_random_entity,
                    get_random_objects)

from django.core.management.base import BaseCommand

from teachers.models import Teacher
from students.models import Student
from groups.models import Group


class Command(BaseCommand):
    # help = 'Generate numbers of teachers'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', type=int, default=100)

    def handle(self, **options):
        count = options.get('count', 0)
        if count:
            try:
                for _ in range(count):
                    teacher = get_random_entity(Teacher, 1).first()
                    students = get_random_entity(Student, randrange(1, 10))
                    headman = get_random_objects(list(students), 1).pop()
                    name = '%s_group' % teacher.fullname
                    group = Group.objects.create(name=name,
                                                 teacher=teacher,
                                                 headman=headman)
                    group.students.set(students)
                    group.save()
            except AttributeError:
                msg = 'Group requires at least 1 Teacher and Student exists!'
                raise Exception(msg)
