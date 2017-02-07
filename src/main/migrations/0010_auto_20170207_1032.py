# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20170207_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 2, 7, 10, 32, 6, 666328), verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='format',
            name='type_format',
            field=models.NullBooleanField(default=True),
        ),
    ]
