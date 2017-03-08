import datetime
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import ModelChoiceField, ModelForm, ModelMultipleChoiceField
from accounts.functions import get_users_of_member_group, get_member_group
from fullcalendar.models import Calendar, Events
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


class CalendarModelForm(ModelForm):
    form_meta = {'title': _("Calendar")}

    group = get_member_group()
    members = get_users_of_member_group()
    workers = User.objects.exclude(groups__in=(group,))

    title = forms.CharField(max_length=100)
    assigned = UserModelChoiceField(members, empty_label="", label=_('assigned to'))
    users = UserModelMultipleChoiceField(workers, label=_('shared with'),widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Calendar
        exclude = ("created_by", "slug")

    def __init__(self, *args, **kwargs):
        super(CalendarModelForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        add_class_time_picker(self, ['max_time', 'min_time'])
        self.fields['users'].widget.attrs.update({'class': ''})



class EventsModelForm(ModelForm):
    form_met = {'title': _('Event')}

    members = get_users_of_member_group()

    title = forms.CharField(max_length=100)
    event_start = forms.DateTimeField(input_formats=['%d/%m/%Y %I:%M %p'])
    event_end = forms.DateTimeField(input_formats=['%d/%m/%Y %I:%M %p'])
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 15}), required=False)
    observation = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 15}), required=False)
    member = UserModelChoiceField(members, empty_label="")

    class Meta:
        model = Events
        exclude = ("is_cancelled", "created_by", "calendar")

    def __init__(self, *args, **kwargs):
        super(EventsModelForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        add_class_time_picker(self, ['event_start', 'event_end'])

