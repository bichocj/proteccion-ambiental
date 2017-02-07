# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20170207_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(verbose_name='date', default=datetime.datetime(2017, 2, 7, 10, 42, 19, 514661)),
        ),
        migrations.AlterField(
            model_name='format',
            name='type_format',
            field=models.IntegerField(null=True, default=1, choices=[(1, 'PLANES'), (2, 'REGISTERS')]),
        ),
    ]
