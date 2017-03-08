import datetime
from django import forms
from django.forms import ModelForm, HiddenInput
from django.utils.translation import ugettext, ugettext_lazy as _

from .functions import add_form_control_class, add_form_text
from .models import Company, Format, Accident, Employee, Requirement


class FormatForm(ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Format
        fields = ['file']


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        add_form_text(self, ('ruc',))
        add_form_control_class(self.fields)


class EmployeeForm(ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    username = forms.CharField(widget=forms.HiddenInput(), required=False, label='')

    class Meta:
        model = Employee
        fields = ('code', 'first_name', 'last_name', 'email', 'password1', 'password2', 'username')

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # self.fields['username'].widget = HiddenInput()
        # self.fields['username'].label = ''
        add_form_control_class(self.fields)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(EmployeeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class AccidentForm(ModelForm):
    class Meta:
        model = Accident
        fields = ['title', 'content', 'type_accident', 'date', 'evidence']

    def __init__(self, *args, **kwargs):
        super(AccidentForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)


class RequirementForm(ModelForm):
    class Meta:
        model = Requirement
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
