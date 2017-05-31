from django.db import models
from django.utils.translation import ugettext as _

from main.models import Company


# //INDICE DE MEJORAS
# VA EN OTROS INDICADORES(OTRO TAB)
# COMO ACUERDO SST
# //INDICE DE CHARLAS PERIODICAS DE SEGURIDAD
# CHARLAS DIARIAS
# N DE CHARLAS PROGRAMADAS
# N DE CHARLAS REALIZADAS
# N DE TRABAJADORES CAPACITADOS
# N DE TRABAJADORES PROGRAMDOS
class Index_de_charlas(models.Model):
    name = models.CharField(max_length=100, null=False, default='INDICE DE CHARLAS PERIODICAS DE SEGURIDAD')

    num_charlas_programadas = models.IntegerField(null=False, blank=False)
    num_charlas_realizadas = models.IntegerField(null=False, blank=False)
    num_trabajadores_capacitados = models.IntegerField(null=False, blank=False)
    num_trabajadores_programados = models.IntegerField(null=False, blank=False)


class Indice_Reporte_Incidente(models.Model):
    name = models.CharField(max_length=100, null=False, default='INCIDE DE REPORTE DE INCIDENTES')

    num_incidentes_peligrosos = models.IntegerField(null=False, blank=False)


class Indice_Inspecciones(models.Model):
    name = models.CharField(max_length=100, null=False, default='INDICE DE INSPECCIONES')
    num_inspeccion_obvs_planeada = models.IntegerField(null=False, blank=False)


class Liderazgo_Participativo(models.Model):
    # RESPONSABLE: [CARGOS]{GERENTE, SUPERVISOR, ASESOR EXTERNO, RECURSOS HUMANOS,COMITE}
    name = models.CharField(max_length=100, null=False, default='INDICE LIDERAZGO PARTICIPATIVO')


class Mejoras_Index(models.Model):
    # RESPONSABLE: [CARGOS]{GERENTE, SUPERVISOR, ASESOR EXTERNO, RECURSOS HUMANOS,COMITE}
    name = models.CharField(max_length=100, null=False, default='INDICE DE MEJORAS')


class No_Conformidades(models.Model):
    # CALENDARIO AUDITORIAS
    # SOLO REPORTE ANUAL
    # TIPO DE AUDITORIA: [INTERNA, EXTERNA]
    # NUMERO DE NO CONFORMIDADES MENORES: NUMERO
    # NUMERO DE NO CONFORMIDADES MAYORES:NUMERO

    INTERNA = 1
    EXTERNA = 2
    type_auditoria = ((INTERNA, 'INTERNA'),
                      (EXTERNA, 'EXTERNA'),)
    name = models.CharField(max_length=100, null=False, default='INDICE DE NO CONFORMIDADES')

    type = models.IntegerField(choices=type_auditoria, null=False, default=INTERNA)
    num_menores = models.IntegerField(null=True, blank=True)
    num_mayores = models.IntegerField(null=True, blank=True)


class Plan_Contingencia(models.Model):
    # DE SIMULCROS Y CAPACITACION[ENTRENAMIENTO]
    # CALENDARIO SIMULACROS
    name = models.CharField(max_length=100, null=False, default='INDICE PLAN DE CONTINGENCIA')


class Medida_IPERC(models.Model):
    # SOLO JUNIO
    # ANUAL

    name = models.CharField(max_length=100, null=False, default='INDICE DE MEDIDAS DE CONTROL IPERC')


class Index(models.Model):
    company = models.ForeignKey(Company)
    indice_no_conformidad = models.ForeignKey(No_Conformidades, null=True)
    indice_plan_contingencia = models.ForeignKey(Plan_Contingencia, null=True)
    indice_medida_iperc = models.ForeignKey(Medida_IPERC, null=True)
    indice_liderazgo = models.ForeignKey(Liderazgo_Participativo, null=True)
    indice_charlas = models.ForeignKey(Index_de_charlas, null=True)
    indice_incidente = models.ForeignKey(Indice_Reporte_Incidente, null=True)
    indice_inpecciones = models.ForeignKey(Indice_Inspecciones, null=True)
    is_using_indice_no_conformidad = models.BooleanField(_('Indice de no Conformidades'), null=False, default=False)
    is_using_plan_contingencia = models.BooleanField(_('Indice plan de contingencia'), null=False, default=False)
    is_using_liderazgo = models.BooleanField(_('Indice Liderazgo Participativo'), null=False, default=False)
    is_using_medida_iperc = models.BooleanField(_('Indice de Medidas de Control IPERC'), null=False, default=False)
    is_using_charlas = models.BooleanField(_('Indice de Charlas Periodicas de Seguridad'), null=False, default=False)
    is_using_incidentes = models.BooleanField(_('Indice de Reporte de Incidentes'), null=False, default=False)
    is_using_inspecciones = models.BooleanField(_('Indice de Inspecciones'), null=False, default=False)
    # is_using_medida_iperc = models.BooleanField(_('Indice de medidas de control IPERC'), null=False, default=False)
    # is_using_medida_iperc = models.BooleanField(_('Indice de medidas de control IPERC'), null=False, default=False)
