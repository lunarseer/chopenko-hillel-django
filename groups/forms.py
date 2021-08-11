from django import forms


class AddGroupForm(forms.Form):

    name = forms.CharField(max_length=30)
    discipline = forms.CharField(max_length=30)
    # students = forms.JSONField(widget = forms.HiddenInput(), required=False)
    # teachers = forms.JSONField(widget = forms.HiddenInput(), required=False)
