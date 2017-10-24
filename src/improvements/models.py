from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from main.models import Company


class Metting(models.Model):
    title = models.CharField(_('title'), max_length=100, null=False, blank=False)
    date = models.DateField(_('date'), null=False, default=datetime.now)
    company = models.ForeignKey(Company, null=False, blank=False, related_name='metting_company')
    percentage = models.DecimalField(_('percentage'), max_digits=10, decimal_places=2, null=True)
    evidence = models.FileField(_('evidence'), upload_to="improvements/meetings/", null=True)


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
