# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('acuerdos_sst', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='percentage',
            field=models.DecimalField(decimal_places=2, null=True, verbose_name='percentage', max_digits=10),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='date_start',
            field=models.DateField(null=True, verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='date_until',
            field=models.DateField(null=True, verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='evidence',
            field=models.FileField(verbose_name='evidence', null=True, upload_to='acuerdos/'),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='state',
            field=models.IntegerField(choices=[(0, 'to do'), (1, 'following'), (2, 'done')], verbose_name='state', default=0),
        ),
        migrations.AlterField(
            model_name='metting',
            name='date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='metting',
            name='evidence',
            field=models.FileField(verbose_name='evidence', null=True, upload_to='acuerdos/reuniones'),
        ),
        migrations.AlterField(
            model_name='metting',
            name='percentage',
            field=models.DecimalField(decimal_places=2, null=True, verbose_name='percentage', max_digits=10),
        ),
    ]
