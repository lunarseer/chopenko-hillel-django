from django.db import models
from django import forms

# Create your models here.


class GenericModel(models.Model):

    def itemname(self):
        return self.__class__.__name__

    def values(self):
        def valid(key):
            if key not in ["_state"]:
                return True
            return None

        return {k: v for k, v in self.__dict__.items() if valid(k)}

    class Meta:
        abstract = True


class GenericPerson(GenericModel):

    firstname = models.CharField(max_length=30, default='John')
    lastname = models.CharField(max_length=30, default='Doe')
    age = models.IntegerField(default=16)

    def __str__(self):
        return "{} {}".format(self.firstname,
                              self.lastname)

    class Meta:
        abstract = True


class Student(GenericPerson):
    pass


class Teacher(GenericPerson):
    dicsiplines = models.JSONField(default=list)


class Group(GenericModel):

    name = models.CharField(max_length=30, default='unnamed group')
    discipline = models.CharField(max_length=30, default='unnamed group')
    students = forms.JSONField()
    teachers = forms.JSONField()

    def __str__(self):
        return "{} - {}".format(self.discipline, self.name)
