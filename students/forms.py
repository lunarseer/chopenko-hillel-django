from typing import List
from django import forms
from .models import *


class PersonInGroupForm(forms.Form):
    pass

class AddStudentForm(forms.Form):
    firstname = forms.CharField(label='First Name', max_length=30)
    lastname = forms.CharField(label='Last Name', max_length=30)
    age = forms.IntegerField(label='Age',min_value=16, max_value=100)


class AddTeacherForm(AddStudentForm):
    pass


class AddGroupForm(forms.Form):

    name = forms.CharField(max_length=30)
    discipline = forms.CharField(max_length=30)
    students = forms.JSONField(widget = forms.HiddenInput(), required=False)
    teachers = forms.JSONField(widget = forms.HiddenInput(), required=False)
