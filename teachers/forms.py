from django.forms import ModelForm

from common.forms import AddPersonForm
from .models import Teacher


class AddTeacherForm(AddPersonForm):
    pass


class TeacherFormFromModel(ModelForm):
    class Meta:
        model = Teacher
        fields = ['firstname', 'lastname', 'age', 'phone', 'disciplines']
