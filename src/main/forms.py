import datetime
from django import forms
from django.forms import ModelForm

from .functions import add_form_control_class, add_form_text
from .models import Company, Format, Accident


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


class DateInput(forms.DateInput):
    input_type = 'date'


class AccidentForm(forms.ModelForm):
    class Meta:
        model = Accident
        fields = ('title', 'content', 'type_accident', 'date')
        widgets = {
            'date': DateInput(),
        }


