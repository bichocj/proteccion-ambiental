from django import forms 
from django.contrib.auth.models import User
from django.forms import ModelForm

class UploadForm(forms.Form):
	filename = forms.CharField(max_length=100)
	docfile = forms.FileField(
        label='Selecciona un archivo'
    )