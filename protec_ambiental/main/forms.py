from django import forms 
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Company
from .functions import add_form_control_class, add_form_text

class UploadForm(forms.Form):
	filename = forms.CharField(max_length=100)
	document = forms.FileField(
        label='Selecciona un archivo'
    )

class CompanyForm(ModelForm):
	class Meta:
		model = Company
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(CompanyForm, self).__init__(*args, **kwargs)
		add_form_text(self, ('ruc',))
		add_form_control_class(self.fields)
