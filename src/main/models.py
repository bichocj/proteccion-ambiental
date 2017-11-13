# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from sorl.thumbnail import ImageField

# from accounts.models import Worker


GERENTE = 0
SUPERVISOR = 1
ASESOR_EXTERNO = 2
RECURSOS_HUMANOS = 3
COMITE = 4

cargos = (
    (GERENTE, 'GERENTE'),
    (SUPERVISOR, 'SUPERVISOR'),
    (ASESOR_EXTERNO, 'ASESOR EXTERNO'),
    (RECURSOS_HUMANOS, 'RECURSOS HUMANOS'),
    (COMITE, 'COMITE')
)


def upload_image_to(instance, filename):
    filename = os.path.splitext(filename)
    filename = str(instance.ruc) + filename[1]
    return filename


class Company(models.Model):
    ruc = models.IntegerField(_('R.U.C.'), null=False, blank=False, unique=True)
    name = models.CharField(_('Nombre Compañia'), max_length=100, null=False, blank=False, unique=True)
    short_name = models.CharField(_('Nombre Corto'), max_length=100, null=False, blank=False, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, blank=True, null=True, unique=True)

    logo = ImageField(_('Logo'), upload_to=upload_image_to, blank=True, null=True)
    address = models.CharField(_('Dirección'), max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.slug = slugify(self.short_name)
        super(Company, self).save(**kwargs)


class Worker(models.Model):
    name = models.CharField(_('Nombres'), max_length=100, null=False, blank=False)
    last_name = models.CharField(_('Apellidos'), max_length=100, null=True, blank=True, default='')
    code = models.CharField(_('Codigo'), max_length=100, null=False, blank=False)
    company = models.ForeignKey(Company, null=False)
    cargo = models.IntegerField(_('Cargo'), choices=cargos, default=RECURSOS_HUMANOS, null=False)
    photo = models.ImageField(_('photo'), null=True, blank=True, upload_to='photos')
    date_in = models.DateField(_('date in'), null=True, blank=True)
    date_out = models.DateField(_('date out'), null=True, blank=True)

    # estado = models.BooleanField(_('Esta activo'), default=True, null=False)

    def __str__(self):
        return self.name + ' ' + self.last_name


class CountWorker(models.Model):
    month_year = models.DateField(null=True)
    workers = models.IntegerField(_('worker quantity'), default=0)
    hours = models.IntegerField(_('hours worked'), default=0)
    company = models.ForeignKey(Company)


class Product(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)


class Requirement(models.Model):
    PROTECTION = 0
    ENTERPRISE = 1
    type_choice = (
        (PROTECTION, PROTECTION),
        (ENTERPRISE, ENTERPRISE)
    )
    name = models.CharField(_('Nombre Requerimiento'), max_length=100, null=False, blank=False)
    description = models.CharField(_('Descripcion'), max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    type_requirement = models.IntegerField(default=PROTECTION, choices=type_choice, null=False)

    def __str__(self):
        return self.name


class LegalRequirement(models.Model):
    General = 0
    Seguridad = 1
    Salud = 2
    Ergonomia = 3
    Mujer = 4
    Agentes = 5
    Cancer = 6
    Hostigamiento = 7
    Edificacion = 8
    Emergencia = 9
    Inspeccion = 10
    Electricidad = 11
    NTP = 12
    Radiaciones = 13
    Sanitarias = 14
    Transporte = 15
    Normas = 16
    type_registers = (
        (General, 'Generales'),
        (Seguridad, 'Seguridad Ocupacional'),
        (Salud, 'Salud Ocupacional'),
        (Ergonomia, 'Ergonomia'),
        (Mujer, 'Mujer Gestante / Personas con limitaciones'),
        (Agentes, 'Agentes Quimicos / Tabaco'),
        (Cancer, 'Cancer'),
        (Hostigamiento, 'Hostigamiento / Disciminacion / VIH - SIDA'),
        (Edificacion, 'Edificacion'),
        (Emergencia, 'Emergencia'),
        (Inspeccion, 'Inspeccion en el Trabajo'),
        (Electricidad, 'Electricidad'),
        (NTP, 'NTP'),
        (Radiaciones, 'Radiaciones'),
        (Sanitarias, 'Sanitarias / Alimentacion'),
        (Transporte, 'Transporte'),
        (Normas, 'Normas Tecnicas Internacionales / NFPA / Otros')
    )
    CUMPLIO = 0
    NO_CUMPLIO = 1
    state = (
        (CUMPLIO, 'CUMPLIO',),
        (NO_CUMPLIO, 'NO CUMPLIO',)
    )
    type_normativa = models.CharField(_('Tipo Normativa'), max_length=200, null=True, blank=True)
    normativa = models.CharField(_('Codigo Normativa'), max_length=200, null=False, blank=False)
    datepublication = models.DateField(_('Fecha Publicacion'), default=datetime.now)
    entitie = models.ForeignKey(Company)
    title = models.CharField(_('Titulo del Dispositivo Legal'), max_length=200, null=False, blank=False)
    apply = models.TextField(_('Que Aplica?'), null=False, blank=False)
    actual_month = models.CharField(max_length=100, null=False, blank=False)
    evidence = models.FileField(_('Evidencia Registro'), upload_to="legal_requirement/", null=True)
    frecuency = models.CharField(_('Frecuencia'), max_length=200, null=True, blank=True)
    date_last_evaluation = models.DateField(_('Fecha Ultima Evaluacion'), null=True, blank=True)
    responsable = models.CharField(max_length=200, null=True, blank=True)
    cumplimiento = models.DecimalField(_('Cumplimiento (%)'), null=True, blank=True, max_digits=10, decimal_places=2)
    observations = models.TextField(_('Observaciones'), null=True, blank=True)
    type_register = models.IntegerField(_('area/proceso/documento relacionado'), choices=type_registers,
                                        default=General, null=False, blank=False)
    state = models.IntegerField(_('Estado'), choices=state, default=NO_CUMPLIO, null=False, blank=False)
    # responsable = models.ForeignKey(Worker)


class Company_Requirement(models.Model):
    company = models.ForeignKey(Company, null=False)
    requirement = models.ForeignKey(Requirement, null=False)


# class Employee(User):
#     code = models.CharField(_('Codigo'), max_length=50, null=False, blank=False)
#     company = models.ForeignKey(Company, null=False, blank=False)
#     time = models.IntegerField(default=0)
#
#
# Company.user = property(lambda e: Employee.objects.filter(company=e).first())


class Meeting(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=100, null=True, blank=True)


def directiry_path(filename):
    path = os.path.dirname(__file__)
    return path + filename


class Evidence(models.Model):
    filename = models.CharField(max_length=50, null=False)
    file = models.FileField()


class MedicControl(models.Model):
    APTO = 0
    APTO_CON_RESTRICCION = 1
    NO_APTO = 2
    medic_states = (
        (APTO, 'APTO'),
        (APTO_CON_RESTRICCION, 'APTO CON RESTRICCION'),
        (NO_APTO, 'NO APTO')

    )
    AUDITIVA = 0
    CALIDAD = 1
    PROMOCION = 2
    PROTECCION = 3
    PROTECCION_RES = 4
    VIGILANCIA = 5
    PROTECCION_RA = 6
    RIEGO = 7
    medic_program = (
        (AUDITIVA, "CONSERVACION AUDITIVA"),
        (CALIDAD, "CALIDAD DE VIDA"),
        (PROMOCION, "PROMOCION Y PRESERVACION SALUD VISUAL"),
        (PROTECCION, "PROTECCION A LA MUJER GESTANTE Y EN EDAD FERTIL"),
        (PROTECCION_RES, "PROTECCION RESPIRATORIA"),
        (VIGILANCIA, "VIGILANCIA CONTRA TME"),
        (PROTECCION_RA, "PROTECCION RADIACION UV"),
        (RIEGO, "RIESGO GEOLOGICO"),
        (8, "NINGUNO")
    )
    company = models.ForeignKey(Company, null=False, blank=False)
    worker = models.ForeignKey(Worker)
    state = models.IntegerField(_('Estado'), choices=medic_states, default=NO_APTO, null=False, blank=False)
    program = models.IntegerField(_('Programa'), choices=medic_program, default=AUDITIVA, null=False, blank=False)
    evidence = models.FileField(_('Evidencia'), upload_to="examen_medico/", null=True)

    date = models.DateField(_('exam date'), null=False, default=datetime.now)
    date_expiration = models.DateField(_('expiration date'), null=False, default=datetime.now)


class Accident(models.Model):
    FIRST_AID = 1
    MEDIC_ATTENTION = 2
    AID_LOST = 3
    AID_FATAL = 4
    ACCIDENT_5 = 5
    ACCIDENT_6 = 6
    ACCIDENT_7 = 7
    INCIDENT = 7
    TYPE_ACCIDENT_CHOICES = (
        (FIRST_AID, 'ACCIDENTES CON PRIMEROS AUXILIOS'),
        (MEDIC_ATTENTION, 'ACCCIDENTE CON ATENCION MEDICA'),
        (AID_LOST, 'ACCIDENTES CON TIEMPO PERDIDO'),
        (AID_FATAL, 'ACCIDENTES FATALES'),
        (INCIDENT, 'INCIDENTE'),
        (ACCIDENT_5, 'INCIDENTES PELIGROS'),
        (ACCIDENT_6, 'ENFERMEDADES OCUPACIONALES'),
        (ACCIDENT_7, 'ACTOS INSEGUROS'),
    )
    title = models.CharField(_('Titulo'), max_length=100, null=False, blank=False)
    content = models.TextField(_('Descripcion'), null=True, blank=True)
    type_accident = models.IntegerField(_('Tipo de Accidente'), choices=TYPE_ACCIDENT_CHOICES,
                                        default=FIRST_AID)  # NOQA
    date = models.DateField(_('Fecha'), null=False, default=datetime.now)
    lose_days = models.DecimalField(_('Dias Perdidos'), max_digits=5, decimal_places=2, null=True, blank=True)
    company = models.ForeignKey(Company, null=False, blank=False)
    worker = models.ForeignKey(Worker, default=None)
    evidence = models.FileField(_('Evidencia'), upload_to="accident/", null=True)


class AccidentDetail(models.Model):
    accident = models.ForeignKey(Accident)
    worker = models.ForeignKey(Worker)


class Task(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    date_time = models.DateTimeField()
    company = models.ForeignKey(Company, null=False, blank=False)
    type_calendar = models.IntegerField(null=False, blank=False)
    meeting = models.ForeignKey(Meeting, null=True, blank=True)
    charge = models.CharField(max_length=100, null=False, blank=False)  # responsable
    content = models.TextField(null=False, blank=False)  # contenido
    start_time = models.DateTimeField('Fecha de inicio')
    end_time = models.DateTimeField('Fecha final')
    # Falta anadir evidencia de tipo imagen
    # status = models.IntegerField("status", choises = STATUS, default = )
    expiration = models.DateTimeField('Fecha de Expiración')


class Report(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, null=False, blank=False)


class Format(models.Model):
    PLANES = 1
    REGISTERS = 2
    TYPE_FORMAT_CHOICES = (
        (PLANES, 'Planes, Programas y Procedimientos'),
        (REGISTERS, 'Registros y Evidencias')
    )
    requirement = models.ForeignKey(Requirement)
    file = models.FileField(_('Archivo'), upload_to="formatos/", null=False, blank=False)
    type_format = models.IntegerField(_('Tipo'), choices=TYPE_FORMAT_CHOICES, default=PLANES,
                                      null=True)  # is if format is planes or registros
    company = models.ForeignKey(Company, null=True, blank=True)
    name = models.CharField(_('Nombre'), max_length=100, null=False, blank=False)


class HistoryFormats(models.Model):
    format = models.ForeignKey(Format, null=True, blank=True)
    file = models.FileField(upload_to="history/%Y/%m/%d", null=True, blank=True)
    date_time = models.DateTimeField(auto_now=True)


class UseProduct(models.Model):
    task = models.ForeignKey(Task, null=False, blank=False)
    product = models.ForeignKey(Product, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)


# class Work(models.Model):
#     employee = models.ForeignKey(Employee, null=False, blank=False)
#     task = models.ForeignKey(Task, null=False, blank=False)
#     time = models.DateTimeField()


# User.company = property(lambda e: Company.objects.get(employee__pk=e.pk))  # NOQA


class UserCompany(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    company = models.ForeignKey(Company, null=True, blank=True)