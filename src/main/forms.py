from django import forms
from django.forms import ModelForm

from .functions import add_form_control_class, add_form_text
from .models import Company, Format


class FormatForm(ModelForm):
    class Meta:
        model = Format
        fields = ('document',)


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        add_form_text(self, ('ruc',))
        add_form_control_class(self.fields)
