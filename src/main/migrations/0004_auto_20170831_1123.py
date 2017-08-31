# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20170831_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='legalrequirement',
            name='state',
        ),
        migrations.AlterField(
            model_name='historyformats',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 31, 11, 23, 7, 248546)),
        ),
    ]
