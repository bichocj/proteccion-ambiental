# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20170207_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(verbose_name='date', default=datetime.datetime(2017, 2, 7, 10, 40, 1, 79115)),
        ),
        migrations.AlterField(
            model_name='accident',
            name='type_accident',
            field=models.IntegerField(verbose_name='type accident', choices=[(1, 'ACCIDENT'), (2, 'INCIDENT')], default=1),
        ),
        migrations.AlterField(
            model_name='format',
            name='type_format',
            field=models.IntegerField(choices=[(1, 'PLANES'), (2, 'REGISTERS')], default=1),
        ),
    ]
