from django.forms import ModelForm, forms
from django.utils.translation import ugettext as _

from acuerdos_sst.models import Agreement, AgreementDetail, Metting
from main.forms import DateInputWidget
from main.functions import add_form_control_class


class MettingForm(ModelForm):
    date = forms.Field(widget=DateInputWidget, label=_('date'))

    class Meta:
        model = Metting
        fields = ['title', 'date']

    def __init__(self, *args, **kwargs):
        super(MettingForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)
        # self.fields['date'].widget.attrs['class'] = 'form-control input-datepicker'


class AgreementForm(ModelForm):
    date = forms.Field(widget=DateInputWidget, label=_('date'))

    class Meta:
        model = Agreement
        fields = ['number', 'title', 'content', 'date', 'owner', 'observations']

    def __init__(self, *args, **kwargs):
        super(AgreementForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)
        # self.fields['title'].widget.attrs['class'] = 'form-control'
        # self.fields['content'].widget.attrs['class'] = 'form-control'
        # self.fields['date'].widget.attrs['class'] = 'form-control input-datepicker'


class AgreementDetailForm(ModelForm):
    evidence = forms.FileField(required=False)

    date_start = forms.Field(widget=DateInputWidget, label=_('start date'))
    date_until = forms.Field(widget=DateInputWidget, label=_('end date'))

    class Meta:
        model = AgreementDetail
        fields = ['description', 'date_start', 'date_until', 'state', 'evidence', 'owner']
        # widgets = {
        #     'date_start': DateInputWidget
        # 'date_start': DateInput(attrs={'type': 'date'}, format='%m-%d-%Y')
        # }

    def __init__(self, *args, **kwargs):
        super(AgreementDetailForm, self).__init__(*args, **kwargs)
        # _instance = kwargs.pop('instance', None)
        # self.fields['description'].widget.attrs['class'] = 'form-control'
        # self.fields['date_until'].widget.attrs['class'] = 'form-control input-datepicker'
        # self.fields['date_start'].widget.attrs['class'] = 'form-control input-datepicker'
        # self.fields['state'].widget.attrs['class'] = 'form-control'
        # self.fields['evidence'].widget.attrs['class'] = 'form-control'
        add_form_control_class(self.fields)
