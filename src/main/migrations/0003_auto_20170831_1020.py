# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170831_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyformats',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 31, 10, 20, 33, 371489)),
        ),
    ]
