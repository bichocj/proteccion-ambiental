# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170125_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyformats',
            name='requirement',
            field=models.ForeignKey(blank=True, to='main.Requirement', null=True),
        ),
    ]
