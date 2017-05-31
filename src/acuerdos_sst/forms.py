from django.forms import ModelForm

from acuerdos_sst.models import Agreement, AgreementDetail


class AgreementForm(ModelForm):
    class Meta:
        model = Agreement
        fields = ['title', 'content', 'date']

    def __init__(self, *args, **kwargs):
        super(AgreementForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.attrs['class'] = 'form-control input-datepicker'


class AgreementDetailForm(ModelForm):
    class Meta:
        model = AgreementDetail
        fields = ['description', 'date_until', 'date_start', 'state', 'evidence']

    def __init__(self, *args, **kwargs):
        super(AgreementDetailForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['date_until'].widget.attrs['class'] = 'form-control input-datepicker'
        self.fields['date_start'].widget.attrs['class'] = 'form-control input-datepicker'
        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['evidence'].widget.attrs['class'] = 'form-control'
