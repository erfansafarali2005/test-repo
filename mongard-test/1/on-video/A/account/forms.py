from django import forms
from django.contrib.auth.models import User

class UserRegisterationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

