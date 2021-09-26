from django import forms
from .validators import phone_validator


class GeneratorCountForm(forms.Form):
    count = forms.IntegerField(min_value=1, max_value=100, required=True)


class AddPersonForm(forms.Form):
    firstname = forms.CharField(label='First Name', max_length=30)
    lastname = forms.CharField(label='Last Name', max_length=30)
    age = forms.IntegerField(label='Age', min_value=16, max_value=100)
    phone = forms.CharField(label='Phone',
                            validators=[phone_validator],
                            required=False)


class ContactForm(forms.Form):
    send_from = forms.CharField(label='From', max_length=100)
    subject = forms.CharField(label='Subject', max_length=200)
    message = forms.CharField(label='Message',
                              max_length=200,
                              widget=forms.Textarea)


class ConfirmActionForm(forms.Form):
    btn = forms.CharField()
