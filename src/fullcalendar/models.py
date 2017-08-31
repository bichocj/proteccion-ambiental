from django.contrib.auth.models import Group, User
from django.db import models
from django.template import defaultfilters
from django.utils.translation import ugettext as _

from main.models import Company, Worker
from proteccion_ambiental.settings import COMPANY_JRA_SLUG


class Calendar(models.Model):
    CAPACITATION = 1
    INSPECTION = 2
    SIMULATION = 3
    OTRO = 4
    CHARLAS = 5
    DOCTOR=6
    types_calendar = ((CAPACITATION, 'CAPACITACION'),
                      (INSPECTION, 'INSPECCION'),
                      (SIMULATION, 'SIMULACRO'),
                      (CHARLAS, 'CHARLAS DE SEGURIDAD'),
                      (OTRO, 'OTRO'),
                      (DOCTOR,'DOCTOR'))
    title = models.CharField(_('Nombre'), max_length=200, null=False, blank=None)
    company = models.ForeignKey(Company, null=False)
    slug = models.SlugField(max_length=100)
    type = models.IntegerField(_('Tipo'), choices=types_calendar, null=False, default=OTRO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Calendar')
        verbose_name_plural = _('Calendars')
        permissions = (
            ("view_calendars", "Can see existing calendars"),
        )

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(self.title)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exists = Calendar.objects.get(slug=slug)
                    if slug_exists:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Calendar.DoesNotExist:
                    self.slug = slug
                    break
        super(Calendar, self).save(*args, **kwargs)


class Accessibility(models.Model):
    calendar = models.ForeignKey(Calendar)
    group = models.ForeignKey(Group)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventType(models.Model):
    CAPACITATION = 1
    INSPECTION = 2
    SIMULATION = 3
    types_event = ((CAPACITATION, 'CAPACITACION'),
                   (INSPECTION, 'INSPECCION'),
                   (SIMULATION, 'SIMULACRO'),)
    name = models.IntegerField(choices=types_event, default=CAPACITATION, null=False)


class Events(models.Model):
    CAPACITATION = 1
    INSPECTION = 2
    SIMULATION = 3
    OTRO = 4
    CHARLAS = 5
    REALIZADO = 2
    PENDIENTE = 1
    DOCTOR=6
    types_event = ((CAPACITATION, 'CAPACITACION'),
                   (INSPECTION, 'INSPECCION'),
                   (SIMULATION, 'SIMULACRO'),
                   (CHARLAS, 'CHARLAS DE SEGURIDAD'),
                   (OTRO, 'OTRO'),
                   (DOCTOR,'DOCTOR'))
    state_event = ((REALIZADO, 'REALIZADO'),
                   (PENDIENTE, 'PENDIENTE'),
                   )
    INDUCCION = 1
    CAPACITACION_DE_LEY = 2
    CAPACITACION_ESPECIFICA = 3
    CAPACITACION_DE_SALUD_OCUPACIONAL = 4
    ENTRENAMIENTO = 5

    type_capacitation = (
        (INDUCCION, 'INDUCCION'),
        (CAPACITACION_DE_LEY, 'CAPACITACION DE LEY'),
        (CAPACITACION_ESPECIFICA, 'CAPACITACION'),
        (CAPACITACION_DE_SALUD_OCUPACIONAL, 'CAPACITACION DE SALUD OCUPACIONAL'),
        (ENTRENAMIENTO, 'ENTRENAMIENTO'),
    )

    INSPECCION_DE_SEGURIDAD = 1
    INSPECCION_DE_SALUD = 2
    INSPECCION_OBSERVACION_PLANEADA = 3
    type_inspeccion = (
        (INSPECCION_DE_SEGURIDAD, 'INSPECCION DE SEGURIDAD'),
        (INSPECCION_DE_SALUD, 'INSPECCION DE SALUD'),
        (INSPECCION_OBSERVACION_PLANEADA, 'INSPECCION OBSERVACION PLANEADA'),

    )
    ASESOR = 0
    COMITE = 1
    RRHH = 2
    SEGURIDAD = 3
    MEDICO = 4
    OPERACIONES = 5
    responsables = (
        (ASESOR, "ASESOR EXTERNO"),
        (COMITE, "COMITE SST"),
        (RRHH, "RR.HH."),
        (SEGURIDAD, "ING. SEGURIDAD"),
        (MEDICO, "MEDICO OCUPACIONAL"),
        (OPERACIONES, "JEFE DE OPERACIONES")

    )
    calendar = models.ForeignKey(Calendar)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    observation = models.TextField(blank=True, null=True)
    type = models.IntegerField(_('Tipo Evento'), choices=types_event, default=CAPACITATION, null=False)
    state = models.IntegerField(_('Estado'), choices=state_event, default=PENDIENTE, null=False)
    responsable = models.IntegerField(_('Responsable'), choices=responsables, null=False, default=ASESOR)
    evidence = models.FileField(_('Evidencia'), upload_to="eventos/", null=True)

    is_cancelled = models.BooleanField(default=False)
    hours_worked = models.FloatField(_('Horas Trabajadas: '), null=True, blank=True)
    number_workers = models.IntegerField(_('Numero de Trabajadores: '), null=True, blank=True)

    created_by = models.ForeignKey(User, related_name="created_by_event")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    type_capacitations = models.IntegerField(_('Tipo Capacitacion'), choices=type_capacitation, null=True, blank=True,
                                             default=INDUCCION)
    type_inspeccions = models.IntegerField(_('TIpo Inspeccion'), choices=type_inspeccion, null=True, blank=True,
                                           default=INSPECCION_DE_SEGURIDAD)
