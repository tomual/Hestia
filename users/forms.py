from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class UserForm(forms.Form):
    username = forms.CharField(min_length=3)
    email = forms.EmailField(min_length=10)
    location = forms.CharField(required=False)
    description = forms.CharField(required=False)
    icon = forms.ImageField(required=False)

class RegisterForm(forms.Form):	
    username = forms.RegexField(min_length=3, max_length=15, regex=r'^[a-zA-Z0-9]+$', error_messages={ 'invalid': _("Username may only contain letters and numbers") })
    email = forms.EmailField(min_length=10)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password Confirm")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username taken")
        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords do not match')
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use")
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)