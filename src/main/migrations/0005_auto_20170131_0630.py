# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170130_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 1, 31, 6, 30, 48, 207628), verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='accident',
            name='type_accident',
            field=models.IntegerField(default=1, verbose_name='type accident', choices=[(1, 'HIGH_WORK'), (2, 'INTOXICATION')]),
        ),
    ]
