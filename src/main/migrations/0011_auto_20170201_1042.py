# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20170131_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(verbose_name='date', default=datetime.datetime(2017, 2, 1, 10, 42, 0, 464691)),
        ),
        migrations.AlterField(
            model_name='accident',
            name='evidence',
            field=models.FileField(verbose_name='evidence', upload_to='accident/', null=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
