from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from main.models import Company


class Person(User):
    MAN = 0
    WOMAN = 1

    SEX = (
        (MAN, _('man')),
        (WOMAN, _('woman')),
    )

    # TODO dni turn it to unique
    # TODO dni show in patient
    dni = models.IntegerField(null=True, blank=True)
    sex = models.IntegerField(_("sex"), choices=SEX, default=MAN)

    def __str__(self):
        return self.get_full_name() + ' | ' + self.email

        # TODO clean_dni


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


class Worker(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.IntegerField(null=False, blank=False)
    company = models.ForeignKey(Company, null=False)
    cargo = models.IntegerField(choices=cargos, default=RECURSOS_HUMANOS, null=False)

    def __str__(self):
        return self.name
