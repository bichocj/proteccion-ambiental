# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20170131_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 1, 31, 7, 1, 36, 638370), verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='accident',
            name='evidence',
            field=models.FileField(upload_to='', null=True),
        ),
    ]
