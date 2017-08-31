# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170831_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='legalrequirement',
            name='state',
            field=models.IntegerField(choices=[(0, 'CUMPLIO'), (1, 'NO CUMPLIO')], default=1, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='historyformats',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 31, 11, 23, 33, 609508)),
        ),
    ]
