from typing import List
from django import forms
from .models import *


class PersonInGroupForm(forms.Form):
    pass

class AddStudentForm(forms.Form):
    firstname = forms.CharField(label='First Name', max_length=30)
    lastname = forms.CharField(label='First Name', max_length=30)
    age = forms.IntegerField(label='Age',min_value=16, max_value=100)


class AddTeacherForm(AddStudentForm):
    pass


class AddGroupForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__()

        self.fields['name'] = forms.CharField(max_length=30)
        self.fields['students'] = forms.MultipleChoiceField(required=False,
                                            choices=kwargs.get('students', []))
        self.fields['teachers'] = forms.MultipleChoiceField(required=False,
                                            choices=kwargs.get('teachers', []))
