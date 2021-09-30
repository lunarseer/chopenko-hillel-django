from common.forms import AddPersonForm
from common.validators import phone_validator

from django.forms import ModelForm, CharField

from .models import Student


class StudentAddForm(AddPersonForm):
    pass


class StudentFormFromModel(ModelForm):
    phone = CharField(required=False)

    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'age', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone_validator(phone)
        return phone
