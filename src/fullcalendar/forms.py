import datetime
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import ModelChoiceField, ModelForm, ModelMultipleChoiceField, HiddenInput
from accounts.functions import get_users_of_member_group, get_member_group
from fullcalendar.models import Calendar, Events, type_capacitation, type_inspeccion, INSPECTION, CAPACITATION, CHARLAS
from main.functions import add_form_control_class, add_class_time_picker
from django.utils.translation import ugettext as _

from main.models import Company

__author__ = 'jona'


class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.first_name:
            name = obj.first_name + " " + obj.last_name
        else:
            name = obj.username
        return name


class UserModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        if obj.first_name:
            name = obj.first_name + " " + obj.last_name
        else:
            name = obj.username
        try:
            name += " | " + obj.company.name
        except Company.DoesNotExist:
            pass
        return name


class WorkerModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        if obj.name:
            name = obj.name + " " + obj.last_name
        else:
            name = obj.code
        return name


class CalendarModelForm(ModelForm):
    form_meta = {'title': _("Calendar")}

    class Meta:
        model = Calendar
        fields = ["title", "type"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CalendarModelForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        if user:
            group = Group.objects.get(name="Doctor")
            if group in user.groups.all():
                self.fields['type'] = forms.IntegerField(label="Tipo", required=False,
                                                         widget=forms.TextInput(
                                                             attrs={'placeholder': 'Doctor', 'readonly': True}))

        add_form_control_class(self.fields)


class EventsModelForm(ModelForm):
    form_met = {'title': _('Event')}

    title = forms.CharField(max_length=100, label="Nombre")
    event_start = forms.DateTimeField(input_formats=['%d/%m/%Y %I:%M %p'], label=_('Comienza '))
    event_end = forms.DateTimeField(input_formats=['%d/%m/%Y %I:%M %p'], label=('Termina '))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 15}), required=False,
                                  label=_('Descripcion '))
    observation = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 15}), required=False,
                                  label="Observacion")
    type_capacitations = forms.ChoiceField(choices=type_capacitation, label='Tipo de Capacitacion',
                                           widget=forms.HiddenInput(), required=False)
    type_inspeccions = forms.ChoiceField(choices=type_inspeccion, label='Tipo de Inspeccion',
                                         widget=forms.HiddenInput(), required=False)
    hours_worked = forms.FloatField(widget=forms.HiddenInput(), required=False)
    number_workers = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    evidence = forms.FileField(label="Evidencia", required=False)

    class Meta:
        model = Events
        exclude = ("is_cancelled", "created_by", "calendar", "type")

    def __init__(self, *args, **kwargs):
        calendar = kwargs.pop('calendar', None)
        super(EventsModelForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_class_time_picker(self, ['event_start', 'event_end'])
        # if _instance and _instance.calendar.type == Calendar.CAPACITATION:
        #     self.fields['type_capacitations'] = forms.ChoiceField(choices=Events.type_capacitation)
        if calendar and (calendar.type == CAPACITATION or calendar.type == CHARLAS):
            self.fields['hours_worked'] = forms.FloatField(label='Horas Trabajadas', required=False)
            self.fields['number_workers'] = forms.IntegerField(label='Numero de Trabajadores', required=False)

        if calendar and calendar.type == CAPACITATION:
            self.fields['type_capacitations'] = forms.ChoiceField(choices=type_capacitation,
                                                                  label='Tipo de Capacitacion', required=True,
                                                                  initial=-1, widget=forms.Select())

        if calendar and calendar.type == INSPECTION:
            self.fields['type_inspeccions'] = forms.ChoiceField(choices=type_inspeccion,
                                                                label='Tipo de Inspeccion', required=True, initial=-1,
                                                                widget=forms.Select())
        add_form_control_class(self.fields)
