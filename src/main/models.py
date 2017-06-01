# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _

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
    ruc = models.IntegerField(null=False, blank=False, unique=True)
    name = models.CharField(_('company name'), max_length=100, null=False, blank=False, unique=True)
    short_name = models.CharField(_('short name'), max_length=100, null=False, blank=False, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, blank=True, null=True, unique=True)
    logo = models.ImageField(_('logo'), upload_to=upload_image_to, blank=True, null=True)
    address = models.CharField(_('address'), max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.slug = slugify(self.short_name)
        super(Company, self).save(**kwargs)


class Worker(models.Model):
    name = models.CharField(_('Nombre'), max_length=100, null=False, blank=False)
    code = models.CharField(_('Codigo'), max_length=100, null=False, blank=False)
    company = models.ForeignKey(Company, null=False)
    cargo = models.IntegerField(_('Cargo'), choices=cargos, default=RECURSOS_HUMANOS, null=False)
    is_active = models.BooleanField(_('Esta Activo?'),default=True, null=False)

    def __str__(self):
        return self.name


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
    normativa = models.CharField(max_length=50, null=False, blank=False)
    datepublication = models.DateTimeField(default=datetime.now)
    entitie = models.ForeignKey(Company)
    title = models.CharField(max_length=200, null=False, blank=False)
    apply = models.TextField(null=False, blank=False)
    actual_month = models.CharField(max_length=100, null=False, blank=False)
    # responsable = models.ForeignKey(Worker)


class Company_Requirement(models.Model):
    company = models.ForeignKey(Company, null=False)
    requirement = models.ForeignKey(Requirement, null=False)


class Employee(User):
    code = models.CharField(max_length=50, null=False, blank=False)
    company = models.ForeignKey(Company, null=False, blank=False)
    time = models.IntegerField(default=0)


Company.user = property(lambda e: Employee.objects.filter(company=e).first())


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
    company = models.ForeignKey(Company, null=False, blank=False)
    worker = models.ForeignKey(Worker)
    state = models.IntegerField(choices=medic_states, default=NO_APTO, null=False, blank=False)
    date = models.DateField(null=False, default=datetime.now)
    evidence = models.FileField(_('Evidencia'), upload_to="examen_medico/", null=True)


class Accident(models.Model):
    ACCIDENT_1 = 1
    ACCIDENT_2 = 2
    ACCIDENT_3 = 3
    ACCIDENT_4 = 4
    ACCIDENT_5 = 5
    ACCIDENT_6 = 6
    TYPE_ACCIDENT_CHOICES = (
        (ACCIDENT_1, 'ACCIDENTES CON PRIMEROS AXILIOS'),
        (ACCIDENT_2, 'ACCCIDENTE CON ATENCION MEDICA'),
        (ACCIDENT_3, 'ACCIDENTES CON TIEMPO PERDIDO'),
        (ACCIDENT_4, 'ACCIDENTES FATALES'),
        (ACCIDENT_5, 'INCIDENTES PELIGROS'),
        (ACCIDENT_6, 'ENFERMEDADES OCUPACIONALES'),
    )
    title = models.CharField(_('Titulo'), max_length=100, null=False, blank=False)
    content = models.TextField(_('Descripcion'), null=True, blank=True)
    type_accident = models.IntegerField(_('Tipo de Accidente'), choices=TYPE_ACCIDENT_CHOICES,
                                        default=ACCIDENT_1)  # NOQA
    date = models.DateField(_('Fecha'), null=False, default=datetime.now)
    lose_days = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    company = models.ForeignKey(Company, null=False, blank=False)
    evidence = models.FileField(_('Evidencia'), upload_to="accident/", null=True)


class Task(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    date_time = models.DateTimeField()
    company = models.ForeignKey(Company, null=False, blank=False)
    type_calendar = models.IntegerField(null=False, blank=False)
    meeting = models.ForeignKey(Meeting, null=True, blank=True)
    charge = models.CharField(max_length=100, null=False, blank=False)  # responsable
    content = models.TextField(null=False, blank=False)  # contenido
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # Falta anadir evidencia de tipo imagen
    # status = models.IntegerField("status", choises = STATUS, default = )
    expiration = models.DateTimeField()


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
    file = models.FileField(upload_to="formatos/", null=False, blank=False)
    type_format = models.IntegerField(choices=TYPE_FORMAT_CHOICES, default=PLANES,
                                      null=True)  # is if format is planes or registros
    company = models.ForeignKey(Company, null=True, blank=True)
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)


class HistoryFormats(models.Model):
    format = models.ForeignKey(Format, null=True, blank=True)
    file = models.FileField(upload_to="history/%Y/%m/%d", null=True, blank=True)
    date_time = models.DateTimeField(default=datetime.now())


class UseProduct(models.Model):
    task = models.ForeignKey(Task, null=False, blank=False)
    product = models.ForeignKey(Product, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)


class Work(models.Model):
    employee = models.ForeignKey(Employee, null=False, blank=False)
    task = models.ForeignKey(Task, null=False, blank=False)
    time = models.DateTimeField()


User.company = property(lambda e: Company.objects.get(employee__pk=e.pk))  # NOQA
