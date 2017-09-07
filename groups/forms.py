from django import forms

class GroupForm(forms.Form):
    name = forms.CharField(min_length=10, max_length=50)
    description = forms.CharField(min_length=10)
    icon = forms.ImageField(required=False)