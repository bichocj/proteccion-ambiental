# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyformats',
            name='document',
            field=models.FileField(null=True, upload_to=b'history/%Y/%m/%d', blank=True),
        ),
        migrations.AlterField(
            model_name='historyformats',
            name='company',
            field=models.ForeignKey(blank=True, to='main.Company', null=True),
        ),
        migrations.AlterField(
            model_name='historyformats',
            name='requirement',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
