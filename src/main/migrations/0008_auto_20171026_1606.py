# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20171024_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countworker',
            name='quantity',
        ),
        migrations.AddField(
            model_name='countworker',
            name='hours',
            field=models.IntegerField(default=0, verbose_name='hours worked'),
        ),
        migrations.AddField(
            model_name='countworker',
            name='workers',
            field=models.IntegerField(default=0, verbose_name='cantidad de trabajadores'),
        ),
    ]
