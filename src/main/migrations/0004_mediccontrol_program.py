# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20171024_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediccontrol',
            name='program',
            field=models.IntegerField(default=0, choices=[(0, 'CONSERVACION AUDITIVA'), (1, 'CALIDAD DE VIDA'), (2, 'PROMOCION Y PRESERVACION SALUD VISUAL'), (3, 'PROTECCION A LA MUJER GESTANTE Y EN EDAD FERTIL'), (4, 'PROTECCION RESPIRATORIA'), (5, 'VIGILANCIA CONTRA TME'), (6, 'PROTECCION RADIACION UV'), (7, 'RIESGO GEOLOGICO')], verbose_name='Programa'),
        ),
    ]
