from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateTimeField, Field
from django.utils.translation import ugettext as _

from accounts.models import Person
from main.forms import DateInputWidget
from main.models import Worker
from main.functions import add_form_control_class


class PasswordChangeFormEdited(PasswordChangeForm):
    meta = {'title': _('Change password'), 'button': _('Save'), 'action': '',
            'form_class': 'col-lg-8 col-lg-offset-2', 'header_class': 'header-form-profile'}

    def __init__(self, *args, **kwargs):
        super(PasswordChangeFormEdited, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': self.fields['old_password'].label})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control input_reset_password', 'placeholder': self.fields['new_password1'].label})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control input_reset_password', 'placeholder': self.fields['new_password2'].label})


class WorkerForm(ModelForm):
    date_in = Field(widget=DateInputWidget, label=_('date in'))
    date_out = Field(widget=DateInputWidget, label=_('date out'))

    class Meta:
        model = Worker
        exclude = ('company',)

    def __init__(self, *args, **kwargs):
        super(WorkerForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)


# class WorkerEditForm(ModelForm):
#     class Meta:
#         model = Worker
#         fields = ['name', 'last_name', 'code', 'cargo', 'photo']
#
#     def __init__(self, *args, **kwargs):
#         super(WorkerEditForm, self).__init__(*args, **kwargs)
#         _instance = kwargs.pop('instance', None)
#         add_form_control_class(self.fields)


class PasswordResetFormEdited(PasswordResetForm):
    meta = {'title': _('Reset password'), 'button': _('Reset'), 'action': '',
            'form_class': 'col-lg-8 col-lg-offset-2', 'header_class': 'header-form-profile'}

    def __init__(self, *args, **kwargs):
        super(PasswordResetFormEdited, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control input_reset_password', 'placeholder': self.fields['email'].label})


class SetPasswordFormEdited(SetPasswordForm):
    meta = {'title': _('Reset password'), 'button': _('Save'), 'action': '',
            'form_class': 'col-lg-8 col-lg-offset-2', 'header_class': 'header-form-profile'}

    def __init__(self, *args, **kwargs):
        super(SetPasswordFormEdited, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control form-first input_reset_password',
                                                          'placeholder': self.fields['new_password1'].label})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control form-last input_reset_password', 'placeholder': self.fields['new_password2'].label})


class AuthenticationFormEdited(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationFormEdited, self).__init__(*args, **kwargs)
        self.fields['username'].label = _('email')
        add_form_control_class(self.fields)
