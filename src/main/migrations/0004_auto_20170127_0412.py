# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20170127_0346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historyformats',
            name='company',
        ),
        migrations.RemoveField(
            model_name='historyformats',
            name='requirement',
        ),
        migrations.AddField(
            model_name='historyformats',
            name='format',
            field=models.ForeignKey(blank=True, to='main.Format', null=True),
        ),
    ]
