# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accessibility',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Nombre', blank=None)),
                ('slug', models.SlugField(max_length=100)),
                ('type', models.IntegerField(choices=[(1, 'CAPACITACION'), (2, 'INSPECCION'), (3, 'SIMULACRO'), (5, 'CHARLAS DE SEGURIDAD'), (4, 'OTRO'), (6, 'DOCTOR')], default=4, verbose_name='Tipo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Calendars',
                'verbose_name': 'crear calendario',
                'permissions': (('view_calendars', 'Can see existing calendars'),),
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('event_start', models.DateTimeField()),
                ('event_end', models.DateTimeField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('observation', models.TextField(null=True, blank=True)),
                ('type', models.IntegerField(choices=[(1, 'CAPACITACION'), (2, 'INSPECCION'), (3, 'SIMULACRO'), (5, 'CHARLAS DE SEGURIDAD'), (4, 'OTRO'), (6, 'DOCTOR')], default=1, verbose_name='Tipo Evento')),
                ('state', models.IntegerField(choices=[(2, 'REALIZADO'), (1, 'PENDIENTE')], default=1, verbose_name='Estado')),
                ('responsable', models.IntegerField(choices=[(0, 'ASESOR EXTERNO'), (1, 'COMITE SST'), (2, 'RR.HH.'), (3, 'ING. SEGURIDAD'), (4, 'MEDICO OCUPACIONAL'), (5, 'JEFE DE OPERACIONES')], default=0, verbose_name='Responsable')),
                ('evidence', models.FileField(null=True, verbose_name='Evidencia', upload_to='eventos/')),
                ('is_cancelled', models.BooleanField(default=False)),
                ('hours_worked', models.FloatField(null=True, verbose_name='Horas Trabajadas: ', blank=True)),
                ('number_workers', models.IntegerField(null=True, verbose_name='Numero de Trabajadores: ', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_capacitations', models.IntegerField(choices=[(1, 'INDUCCION'), (2, 'CAPACITACION DE LEY'), (3, 'CAPACITACION'), (4, 'CAPACITACION DE SALUD OCUPACIONAL'), (5, 'ENTRENAMIENTO')], null=True, default=1, verbose_name='Tipo Capacitacion', blank=True)),
                ('type_inspeccions', models.IntegerField(choices=[(1, 'INSPECCION DE SEGURIDAD'), (2, 'INSPECCION DE SALUD'), (3, 'INSPECCION OBSERVACION PLANEADA')], null=True, default=1, verbose_name='TIpo Inspeccion', blank=True)),
                ('calendar', models.ForeignKey(to='fullcalendar.Calendar')),
                ('created_by', models.ForeignKey(related_name='created_by_event', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.IntegerField(choices=[(1, 'CAPACITACION'), (2, 'INSPECCION'), (3, 'SIMULACRO')], default=1)),
            ],
        ),
    ]
