from django.forms import ModelForm

from indices.models import Index
from main.functions import add_form_control_class


class IndexForm(ModelForm):
    class Meta:
        model = Index
        fields = ['is_using_sgsst','is_using_legal','is_using_icsst','is_using_indice_no_conformidad', 'is_using_medida_iperc','is_using_liderazgo','is_using_plan_contingencia','is_using_mejora','is_using_capacitacion','is_using_personal_capacitado','is_using_intensidad_formativa','is_using_charlas','is_using_incidentes','is_using_inspecciones','is_using_observaciones_planeadas','is_using_auditorias','is_using_simulacros_emergencia','is_using_reconocimiento_trabajador','is_using_sgsst']
    def __init__(self, *args, **kwargs):
        super(IndexForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)