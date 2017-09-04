from django import forms

class ImageUploader(forms.Form):
    icon = forms.ImageField()