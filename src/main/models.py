from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _



class Product(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)


class Company(models.Model):
    ruc = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(User):
    code = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    company = models.ForeignKey(Company, null=False, blank=False)
    time = models.IntegerField()



class Meeting(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=100, null=True, blank=True)


class Accident(models.Model):
    HIGH_WORK = 'HIGH_WORK'
    INTOXICATION = 'INTOXICATION'
    TYPE_ACCIDENT_CHOICES = (
        (HIGH_WORK,'HIGH_WORK'),
        (INTOXICATION,'INTOXICATION')
    )
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=True, blank=True)
    type_accident = models.CharField(_('type accident'), max_length=10, choices=TYPE_ACCIDENT_CHOICES, null=True,
                                     default=HIGH_WORK)  # NOQA
    date = models.DateField(_('date'),null=False, default=datetime.now())
    company = models.ForeignKey(Company, null=False, blank=False)


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


class Requirement(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Format(models.Model):
    requirement = models.ForeignKey(Requirement)
    document = models.FileField(upload_to="formatos/%Y/%m/%d", null=False, blank=False)
    company = models.ForeignKey(Company, null=False, blank=False)


class Calendar(models.Model):
    company = models.ForeignKey(Company, null=False, blank=False)


# type_calendar = models.IntegerField("type", choises =TYPE, default = )


class HistoryFormats(models.Model):
#    requirement = models.ForeignKey(Requirement, null = True, blank = True)
    format = models.ForeignKey(Format, null = True, blank = True)
    document = models.FileField(upload_to="history/%Y/%m/%d", null=True, blank=True)
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
