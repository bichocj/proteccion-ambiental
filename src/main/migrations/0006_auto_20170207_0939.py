# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170207_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='format',
            name='type_format',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(verbose_name='date', default=datetime.datetime(2017, 2, 7, 9, 39, 50, 967679)),
        ),
    ]
