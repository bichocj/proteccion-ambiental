# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-04 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('improvements', '0006_auto_20171226_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metting',
            name='applied_to',
            field=models.ManyToManyField(to='improvements.MettingAppliedTo', verbose_name='Aplicado a'),
        ),
    ]
