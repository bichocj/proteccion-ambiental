# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='type_accident',
            field=models.CharField(null=True, max_length=10, choices=[('HIGH_WORK', 'HIGH_WORK'), ('INTOXICATION', 'INTOXICATION')], default='HIGH_WORK', verbose_name='type accident'),
        ),
    ]
