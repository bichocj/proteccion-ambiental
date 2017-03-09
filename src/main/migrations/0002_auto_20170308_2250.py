# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='short_name',
            field=models.CharField(default='', unique=True, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 3, 8, 22, 50, 22, 567366), verbose_name='date'),
        ),
    ]
