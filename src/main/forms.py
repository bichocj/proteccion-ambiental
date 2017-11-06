# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm, HiddenInput
from django.utils.translation import ugettext_lazy as _

from .functions import add_form_control_class, add_form_text, add_form_control2_class
from .models import Company, Format, Accident, Employee, Requirement, LegalRequirement, MedicControl, Worker, \
    AccidentDetail, CountWorker


class FormatForm(ModelForm):
    # file = forms.FileField(required=True)

    class Meta:
        model = Format
        fields = ['name', 'file', 'type_format']

    def __init__(self, *args, **kwargs):
        super(FormatForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('slug',)

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
        fields = ('code', 'email', 'password1', 'password2', 'username')

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


class DateInputWidget(forms.DateInput):
    input_type = 'date'


class LegalRequirementForm(ModelForm):
    class Meta:
        model = LegalRequirement
        fields = ['type_normativa', 'normativa', 'datepublication', 'title', 'apply', 'evidence',
                  'frecuency', 'date_last_evaluation', 'responsable', 'cumplimiento', 'observations', 'type_register',
                  'state']

    def __init__(self, *args, **kwargs):
        super(LegalRequirementForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)
        self.fields['datepublication'].widget.attrs['class'] = 'form-control input-datepicker'
        self.fields['date_last_evaluation'].widget.attrs['class'] = 'form-control input-datepicker'


class MedicControlForm(ModelForm):
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(), label='Trabajador')
    evidence = forms.FileField(required=False, label='Exámen')

    class Meta:
        model = MedicControl
        fields = ['worker', 'state', 'program', 'date','date_expiration', 'evidence']

    def __init__(self, *args, **kwargs):
        super(MedicControlForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)
        self.fields['date'].widget.attrs['class'] = 'form-control input-datepicker'


class AccidentForm(ModelForm):
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(), label='Trabajador')
    evidence = forms.FileField(required=False)
    date = forms.Field(widget=DateInputWidget)

    class Meta:
        model = Accident
        fields = ['title', 'content', 'type_accident', 'worker', 'date', 'evidence']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AccidentForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        if user:
            group = Group.objects.get(name="Doctor")
            if not group in user.groups.all():
                self.fields['evidence'] = forms.Field(widget=HiddenInput, required=False)
        else:
            self.fields['evidence'] = forms.Field(widget=HiddenInput, required=False)
        add_form_control_class(self.fields)
        add_form_control2_class(self.fields['worker'])
        self.fields['date'].widget.attrs['class'] = 'form-control input-datepicker'


class AccidentDetailForm(ModelForm):
    class Meta:
        model = AccidentDetail
        fields = ['worker']

    def __init__(self, *args, **kwargs):
        super(AccidentDetailForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)


class RequirementForm(ModelForm):
    class Meta:
        model = Requirement
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)


class CountWorkerForm(ModelForm):
    class Meta:
        model = CountWorker
        fields = ["workers", 'hours']

    def __init__(self, *args, **kwargs):
        super(CountWorkerForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)
