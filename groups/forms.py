from django import forms

class GroupForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=50)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'tinymce'}))
    icon = forms.ImageField(required=False)