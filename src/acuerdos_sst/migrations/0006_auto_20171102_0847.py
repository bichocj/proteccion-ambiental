# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-02 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acuerdos_sst', '0005_auto_20171102_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='observations',
            field=models.TextField(blank=True, null=True, verbose_name='observations'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='number',
            field=models.IntegerField(verbose_name='número de acuerdo'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='owner',
            field=models.IntegerField(choices=[(0, 'ASESOR EXTERNO'), (1, 'COMITE SST'), (2, 'RR.HH.'), (3, 'ING. SEGURIDAD'), (4, 'MEDICO OCUPACIONAL'), (5, 'JEFE DE OPERACIONES'), (6, 'GERENTE GENERAL'), (7, 'SUPERVISOR DE OPERACIONES')], default=0, null=True, verbose_name='responsable'),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='date_start',
            field=models.DateField(null=True, verbose_name='hasta'),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='date_until',
            field=models.DateField(null=True, verbose_name='desde'),
        ),
        migrations.AlterField(
            model_name='agreementdetail',
            name='owner',
            field=models.IntegerField(choices=[(0, 'ASESOR EXTERNO'), (1, 'COMITE SST'), (2, 'RR.HH.'), (3, 'ING. SEGURIDAD'), (4, 'MEDICO OCUPACIONAL'), (5, 'JEFE DE OPERACIONES'), (6, 'GERENTE GENERAL'), (7, 'SUPERVISOR DE OPERACIONES')], default=0, null=True, verbose_name='responsable'),
        ),
    ]