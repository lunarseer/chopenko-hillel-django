from django.forms import ModelForm, CharField

from common.forms import AddPersonForm
from common.validators import phone_validator
from .models import Teacher


class AddTeacherForm(AddPersonForm):
    pass


class TeacherFormFromModel(ModelForm):
    phone = CharField(required=False)

    class Meta:
        model = Teacher
        fields = ['firstname', 'lastname', 'age', 'phone', 'disciplines']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone_validator(phone)
        return phone
