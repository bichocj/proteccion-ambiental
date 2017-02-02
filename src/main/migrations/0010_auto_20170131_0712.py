# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20170131_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(verbose_name='date', default=datetime.datetime(2017, 1, 31, 7, 12, 18, 96342)),
        ),
        migrations.AlterField(
            model_name='accident',
            name='evidence',
            field=models.FileField(null=True, verbose_name='evidence', upload_to='accident/%Y/%m/%d'),
        ),
    ]
