# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20171024_0708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countworker',
            name='month',
        ),
        migrations.RemoveField(
            model_name='countworker',
            name='year',
        ),
        migrations.AddField(
            model_name='countworker',
            name='month_year',
            field=models.DateField(null=True),
        ),
    ]
