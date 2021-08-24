from django import forms

from .models import Group


class AddGroupForm(forms.Form):

    name = forms.CharField(max_length=30)
    discipline = forms.CharField(max_length=30)


class GroupFormFromModel(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'discipline']
