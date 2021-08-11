from django.db import models
from django import forms

from common.models import GenericModel


class Group(GenericModel):

    name = models.CharField(max_length=30, default='unnamed group')
    discipline = models.CharField(max_length=30, default='unnamed discipline')
    students = forms.JSONField()
    teachers = forms.JSONField()

    def __str__(self):
        return "{} - {}".format(self.discipline, self.name)