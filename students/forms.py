from common.forms import AddPersonForm
from django.forms import ModelForm
from .models import Student


class AddStudentForm(AddPersonForm):
    pass


class StudentFormFromModel(ModelForm):
    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'age']