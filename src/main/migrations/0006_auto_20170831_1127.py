# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170831_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyformats',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 31, 11, 27, 15, 575005)),
        ),
    ]
