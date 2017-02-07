# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20170207_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 2, 7, 9, 7, 39, 952628), verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='format',
            name='file',
            field=models.FileField(upload_to='formatos/'),
        ),
    ]
