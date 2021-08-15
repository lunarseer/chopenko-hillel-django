from django import forms

from .models import Group

class AddGroupForm(forms.Form):

    name = forms.CharField(max_length=30)
    discipline = forms.CharField(max_length=30)
    # students = forms.JSONField(widget = forms.HiddenInput(), required=False)
    # teachers = forms.JSONField(widget = forms.HiddenInput(), required=False)


class GroupFormFromModel(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'discipline']
