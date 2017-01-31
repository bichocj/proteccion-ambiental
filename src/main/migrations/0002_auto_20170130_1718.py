# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 1, 30, 17, 18, 22, 269508), verbose_name='date'),
        ),
    ]
