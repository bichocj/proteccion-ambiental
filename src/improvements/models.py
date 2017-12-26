from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from main.models import Company

class MettingAppliedTo(models.Model):    
    name = models.CharField(_('responsable'), max_length=100, null=False, blank=False)
    def __str__(self):
        return self.name

class Metting(models.Model):
    SEGURIDAD = 1
    OPERACIONES = 2
    RRHH = 3
    ACCOUNTING = 4
    GERENTE_GENERAL = 5
    ALL = 6

    APPLIED_TO = (
        (SEGURIDAD, "SEGURIDAD Y SALUD OCUPACIONAL"),
        (OPERACIONES, "OPERACIONES"),
        (RRHH, "RR.HH."),
        (ACCOUNTING, "CONTABILIDAD"),
        (GERENTE_GENERAL, "GERENTE GENERAL"),
        (ALL, "TODOS"),
    )

    CHIEF_SSOMA = 1
    CHIEF_OPERACIONES = 2
    CHIEF_SUPER_OPERACIONES = 3
    CHIEF_RRHH = 4
    CHIEF_ACCOUNTING = 5
    CHIEF_GERENTE_GENERAL = 6

    OWNER = (
        (CHIEF_SSOMA, "Jefe de SSOMA"),
        (CHIEF_OPERACIONES, "Jefe de operaciones"),
        (CHIEF_SUPER_OPERACIONES, "Supervisor de operaciones"),
        (CHIEF_RRHH, "RRHH"),
        (CHIEF_ACCOUNTING, "Contabilidad"),
        (CHIEF_GERENTE_GENERAL, "GERENTE GENERAL"),
    )

    title = models.CharField(_('nombre de la mejora'), max_length=100, null=False, blank=False)
    description = models.TextField(_('descripción'), null=True, blank=True)
    inconvenient = models.TextField(_('inconveniente detectado'), null=True, blank=True)
    propose = models.TextField(_('propuesta'), null=True, blank=True)
    applied_to = models.ManyToManyField(MettingAppliedTo, verbose_name=_('Aplicado a'))
    date = models.DateField(_('fecha de generación de propuesta'), null=False, default=datetime.now)
    owner = models.IntegerField(_('responsable de la mejora'), choices=OWNER, default=CHIEF_GERENTE_GENERAL)
    effectiveness = models.BooleanField(_('efectividad'), default=False)

    company = models.ForeignKey(Company, null=False, blank=False, related_name='metting_company')
    percentage = models.DecimalField(_('percentage'), max_digits=10, decimal_places=2, null=True)
    evidence = models.FileField(_('evidence'), upload_to="improvements/meetings/", null=True, blank=True)

    def __str__(self):
        return self.title
    

class Agreement(models.Model):
    metting = models.ForeignKey(Metting, null=True, blank=True)
    title = models.CharField(_('title'), max_length=100, null=False, blank=False)
    content = models.TextField(_('description'), null=True, blank=True)
    date = models.DateField(_('date'), null=False, default=datetime.now)
    company = models.ForeignKey(Company, null=False, blank=False, related_name='agreement_company')
    is_active = models.BooleanField(null=False, default=True)
    percentage = models.DecimalField(_('percentage'), max_digits=10, decimal_places=2, null=True)


class AgreementDetail(models.Model):
    TO_DO = 0
    DOING = 1
    DONE = 2
    status = (
        (TO_DO, _('to do')),
        (DOING, _('following')),
        (DONE, _('done'))
    )
    agreement = models.ForeignKey(Agreement)
    description = models.TextField(_('description'), null=False, blank=False)
    date_until = models.DateField(_('date until'), null=True)
    date_start = models.DateField(_('date start'), null=True)
    state = models.IntegerField(_('state'), choices=status, default=TO_DO)
    evidence = models.FileField(_('evidence'), upload_to="improvements/", null=True)
