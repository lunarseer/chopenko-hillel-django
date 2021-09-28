from django.db import models

from common.models import GenericModel
from students.models import Student
from teachers.models import Teacher


class Group(GenericModel):

    name = models.CharField(max_length=30, default='unnamed group')
    discipline = models.CharField(max_length=30, default='unnamed discipline')
    students = models.ManyToManyField(Student, related_name='students2group')
    headman = models.ForeignKey(Student,
                                blank=True,
                                null=True,
                                default=None,
                                on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,
                                blank=True,
                                null=True,
                                default=None,
                                on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)

    @property
    def info(self):
        return "{} {}".format(self.__class__.__name__,
                              self.name)
