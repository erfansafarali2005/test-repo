from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
    register_form_username = forms.CharField(max_length=20 , widget=forms.TextInput(attrs={'placeholder' : 'your username'}))
    register_form_email = forms.EmailField(max_length=50 , widget=forms.EmailInput(attrs={'placeholder' : 'your email'}))
    register_form_password1 = forms.CharField(max_length=50 , widget=forms.PasswordInput(attrs={'placeholder' : 'your password'}))
    register_form_password2 = forms.CharField(max_length=50 , widget=forms.PasswordInput(attrs={'placeholder' : 'repeat your password'}))


    def clean_email(self):
        email_clean = self.cleaned_data['regiser_form_email']
        user = User.objects.get(email=email_clean)

        if user:
            return ValidationError('user already registered')
        else:
            return user

    def clean_username(self):
        username_clean = self.cleaned_data['regiser_form_username']
        user = User.objects.get(username = username_clean)

        if user:
            return ValidationError('user already exists')
        else:
            return user

    def clean(self):
        cd = super().clean()
        p1 = cd.get('register_form_password1')
        p2 = cd.get('register_form_password2')

        if p1 and p2 and p1!=p2:
            return ValidationError('passwords do not match')



class UserLoginForm(forms.Form):
    login_form_username_or_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'your username of email'}))
    login_form_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'your password'}))


