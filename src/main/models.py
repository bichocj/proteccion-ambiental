import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Product(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)


class Company(models.Model):
    ruc = models.IntegerField(null=False, blank=False, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, blank=True, null=True, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    is_pricnipal=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Requirement(models.Model):
    PROTECTION = 0
    ENTERPRISE = 1
    type_choice = (
        (PROTECTION, PROTECTION),
        (ENTERPRISE, ENTERPRISE)
    )
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    type_requirement = models.IntegerField(default=PROTECTION, choices=type_choice, null=False)

    def __str__(self):
        return self.name


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


class Accident(models.Model):
    ACCIDENT = 1
    INCIDENT = 2
    TYPE_ACCIDENT_CHOICES = (
        (ACCIDENT, 'ACCIDENT'),
        (INCIDENT, 'INCIDENT')
    )
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=True, blank=True)
    type_accident = models.IntegerField(_('type accident'), choices=TYPE_ACCIDENT_CHOICES, default=ACCIDENT)  # NOQA
    date = models.DateField(_('date'), null=False, default=datetime.now())
    company = models.ForeignKey(Company, null=False, blank=False)
    evidence = models.FileField(_('evidence'), upload_to="accident/", null=True)


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
        (PLANES, 'PLANES'),
        (REGISTERS, 'REGISTERS')
    )
    requirement = models.ForeignKey(Requirement)
    file = models.FileField(upload_to="formatos/", null=False, blank=False)
    type_format = models.IntegerField(choices=TYPE_FORMAT_CHOICES, default=PLANES,
                                      null=True)  # is if format is planes or registros
    company = models.ForeignKey(Company, null=False, blank=False)


class HistoryFormats(models.Model):
    #    requirement = models.ForeignKey(Requirement, null = True, blank = True)
    format = models.ForeignKey(Format, null=True, blank=True)

    file = models.FileField(upload_to="history/%Y/%m/%d", null=True, blank=True)
    #    company = models.ForeignKey(Company, null=True,
    #                                blank=True)  # Clase Compania, el formato es completado de una compania
    date_time = models.DateTimeField()  # La fecha en el que se hizo la modificacion del formato


class UseProduct(models.Model):
    task = models.ForeignKey(Task, null=False, blank=False)
    product = models.ForeignKey(Product, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)


class Work(models.Model):
    employee = models.ForeignKey(Employee, null=False, blank=False)
    task = models.ForeignKey(Task, null=False, blank=False)
    time = models.DateTimeField()


User.company = property(lambda e: Company.objects.get(employee__pk=e.pk))  # NOQA
# Requirement.formats = property(lambda e: Format.objects.filter(requirement__pk=e.pk, company__pk=User.company.pk))  # NOQA
