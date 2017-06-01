from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from main.models import Company


class Agreement(models.Model):
    title = models.CharField(_('Titulo'), max_length=100, null=False, blank=False)
    content = models.TextField(_('Descripcion'), null=True, blank=True)
    date = models.DateField(_('Fecha'), null=False, default=datetime.now)
    company = models.ForeignKey(Company, null=False, blank=False)
    is_active = models.BooleanField(null=False, default=True)
    percentage = models.DecimalField(_('Porcentaje'), max_digits=10, decimal_places=2, null=True)


class AgreementDetail(models.Model):
    TO_DO = 0
    DOING = 1
    DONE = 2
    status = (
        (TO_DO, 'NO CUMPLIDO'),
        (DOING, 'EN SEGUIMIENTO'),
        (DONE, 'CUMPLIO')
    )
    agreement = models.ForeignKey(Agreement)
    description = models.TextField(_('Description'), null=False, blank=False)
    date_until = models.DateField(_('Realizar antes de'), null=True)
    date_start = models.DateField(_('Comenzar'), null=True)
    state = models.IntegerField(_('Estado'), choices=status, default=TO_DO)
    evidence = models.FileField(_('Evidencia'), upload_to="acuerdos/", null=True)

