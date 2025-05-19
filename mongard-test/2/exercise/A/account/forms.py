from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisterationForm(forms.Form):
    form_register_username = forms.CharField(max_length=12,widget=forms.TextInput(attrs={'placeholder':'your username'}))
    form_register_email = forms.EmailField(max_length=40,widget=forms.EmailInput(attrs={'placeholder':'your email'}))
    form_register_password1 = forms.CharField(max_length=20 , widget=forms.PasswordInput(attrs={'placeholder':'your password'}))
    form_register_password2 = forms.CharField(max_length=20 , widget=forms.PasswordInput(attrs={'placeholder':'your password again'}))

    def clean_email(self):
        email = self.cleaned_data['form_register_email']
        user = User.objects.filter(email=email).exists()

        if user:
            raise ValidationError('email already registered')
        else:
            return email

    def clean_username(self):
        username = self.cleaned_data['form_register_username']
        user = User.objects.filter(username=username).exists()

        if user:
            raise ValidationError('username already exists')
        else:
            return username

    def clean(self):
        cd = super().clean()

        p1 = cd['form_register_password1']
        p2 = cd['form_register_password2']

        if p1 and p2 and p1 != p2:
            raise ValidationError('passwords must patch')

class UserLoginForm(forms.Form):
    form_login_username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'your username'}))
    form_login_password = forms.CharField(max_length=20 , widget=forms.PasswordInput(attrs={'placeholder':'your password'}))
