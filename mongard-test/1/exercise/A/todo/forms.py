from django import forms
from .models import Todo

class TodoCreationForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('__all__')
