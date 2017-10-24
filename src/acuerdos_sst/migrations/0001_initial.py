# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20171023_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Titulo')),
                ('content', models.TextField(blank=True, verbose_name='Descripcion', null=True)),
                ('date', models.DateField(verbose_name='Fecha', default=datetime.datetime.now)),
                ('is_active', models.BooleanField(default=True)),
                ('percentage', models.DecimalField(null=True, max_digits=10, verbose_name='Porcentaje', decimal_places=2)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='AgreementDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('description', models.TextField(verbose_name='Descripcion')),
                ('date_until', models.DateField(null=True, verbose_name='Fecha maxima')),
                ('date_start', models.DateField(null=True, verbose_name='Fecha inicio')),
                ('state', models.IntegerField(default=0, verbose_name='Estado', choices=[(0, 'NO CUMPLIDO'), (1, 'EN SEGUIMIENTO'), (2, 'CUMPLIO')])),
                ('evidence', models.FileField(upload_to='acuerdos/', verbose_name='Evidencia', null=True)),
                ('agreement', models.ForeignKey(to='acuerdos_sst.Agreement')),
            ],
        ),
        migrations.CreateModel(
            name='Metting',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Titulo')),
                ('date', models.DateField(verbose_name='Fecha', default=datetime.datetime.now)),
                ('percentage', models.DecimalField(null=True, max_digits=10, verbose_name='Porcentaje', decimal_places=2)),
                ('evidence', models.FileField(upload_to='acuerdos/reuniones/', verbose_name='Evidencia', null=True)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.AddField(
            model_name='agreement',
            name='metting',
            field=models.ForeignKey(blank=True, to='acuerdos_sst.Metting', null=True),
        ),
    ]
