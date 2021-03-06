# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-02 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20171102_0643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='estado',
        ),
        migrations.AlterField(
            model_name='countworker',
            name='hours',
            field=models.IntegerField(default=0, verbose_name='horas trabajadas'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='date_in',
            field=models.DateField(blank=True, null=True, verbose_name='fecha de ingreso'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='date_out',
            field=models.DateField(blank=True, null=True, verbose_name='fecha de salida'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='photo',
            field=models.ImageField(null=True, upload_to='photos', verbose_name='foto'),
        ),
    ]
