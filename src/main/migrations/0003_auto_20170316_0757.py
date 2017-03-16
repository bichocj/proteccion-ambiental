# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170308_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(null=True, verbose_name='logo', blank=True, upload_to=main.models.upload_image_to),
        ),
        migrations.AddField(
            model_name='format',
            name='name',
            field=models.CharField(verbose_name='nombre', default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(verbose_name='date', default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(null=True, verbose_name='address', blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(verbose_name='company name', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='short_name',
            field=models.CharField(verbose_name='short name', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='format',
            name='company',
            field=models.ForeignKey(blank=True, null=True, to='main.Company'),
        ),
        migrations.AlterField(
            model_name='historyformats',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 16, 7, 57, 39, 367564)),
        ),
    ]
