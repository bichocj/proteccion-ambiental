# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('acuerdos_sst', '0002_auto_20171024_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='content',
            field=models.TextField(verbose_name='descripción', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='date',
            field=models.DateField(verbose_name='fecha', default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='percentage',
            field=models.DecimalField(verbose_name='porcentaje', decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='date_start',
            field=models.DateField(verbose_name='fecha inicio', null=True),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='date_until',
            field=models.DateField(verbose_name='fecha fin', null=True),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='description',
            field=models.TextField(verbose_name='descripción'),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='evidence',
            field=models.FileField(verbose_name='evidencia', upload_to='acuerdos/', null=True),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='state',
            field=models.IntegerField(verbose_name='estado', choices=[(0, 'por hacer'), (1, 'en seguimiento'), (2, 'relizado')], default=0),
        ),
        migrations.AlterField(
            model_name='metting',
            name='date',
            field=models.DateField(verbose_name='fecha', default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='metting',
            name='evidence',
            field=models.FileField(verbose_name='evidencia', upload_to='acuerdos/reuniones', null=True),
        ),
        migrations.AlterField(
            model_name='metting',
            name='percentage',
            field=models.DecimalField(verbose_name='porcentaje', decimal_places=2, max_digits=10, null=True),
        ),
    ]
