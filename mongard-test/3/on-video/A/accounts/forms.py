from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreateForm(forms.ModelForm): # this works in admin panel

    password1 = forms.CharField(widget=forms.PasswordInput , label='password')
    password2 = forms.CharField(widget=forms.PasswordInput , label='confirm_password')

    model = User
    class Meta:
        fields = ('email' , 'phone_number' , 'full_name' )

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords must match')
        return cd['password2']

    def save(self , commit=True): #if commit was true
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2']) #hashing password
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm): # this works in admin panel
	password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form</a>.") # we can't change the users password

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegisterationForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField()
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            return ValidationError('this email is already exits')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone)

        if user:
            return ValidationError('this phone is already exists')
        return phone



class VefiyCodeForm(forms.Form):
    code = forms.IntegerField()