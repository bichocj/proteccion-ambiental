from django.forms import ModelForm, ClearableFileInput
from .models import Entrada 

class CustomClearableFielInput(ClearableFileInput):
	template_with_clear = '<br> <label for = "%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'


class FormEntrada(ModelForm):
	class Meta:
		model = Entrada
		fields = ('titulo', 'texto', 'archivo')
		widgets = {
		'archivo': CustomClearableFielInput
		}