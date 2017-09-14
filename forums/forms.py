from django import forms

class ThreadForm(forms.Form):
    title = forms.CharField(min_length=10)
    message = forms.CharField(min_length=10, widget=forms.Textarea(attrs={'class' : 'tinymce'}))

class ResponseForm(forms.Form):
    message = forms.CharField(min_length=10, widget=forms.Textarea(attrs={'class' : 'tinymce'}))