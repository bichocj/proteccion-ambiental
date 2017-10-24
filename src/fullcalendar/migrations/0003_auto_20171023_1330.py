# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fullcalendar', '0002_auto_20170831_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='type',
            field=models.IntegerField(default=1, verbose_name='Tipo Evento', choices=[(1, 'CAPACITACION'), (2, 'INSPECCION'), (3, 'SIMULACRO')]),
        ),
    ]
