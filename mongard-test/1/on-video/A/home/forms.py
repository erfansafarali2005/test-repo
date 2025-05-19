from django import forms
from .models import Todo

class TodoCreateForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField()

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'body']