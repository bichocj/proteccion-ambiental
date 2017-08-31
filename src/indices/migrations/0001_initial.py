# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170831_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('is_using_sgsst', models.BooleanField(default=False, verbose_name='Índice de Cumplimiento del SGSST')),
                ('is_using_legal', models.BooleanField(default=False, verbose_name='Índice Legal')),
                ('is_using_icsst', models.BooleanField(default=False, verbose_name='Implementación CSST')),
                ('is_using_indice_no_conformidad', models.BooleanField(default=False, verbose_name='Indice de no Conformidades')),
                ('is_using_medida_iperc', models.BooleanField(default=False, verbose_name='Indice de Medidas de Control IPERC')),
                ('is_using_liderazgo', models.BooleanField(default=False, verbose_name='Indice Liderazgo Participativo')),
                ('is_using_plan_contingencia', models.BooleanField(default=False, verbose_name='Indice de Actividades del plan de contingencia')),
                ('is_using_mejora', models.BooleanField(default=False, verbose_name='Índice de Mejora')),
                ('is_using_capacitacion', models.BooleanField(default=False, verbose_name='Índice de Capacitacion')),
                ('is_using_personal_capacitado', models.BooleanField(default=False, verbose_name='Índice de Personal Capacitado')),
                ('is_using_intensidad_formativa', models.BooleanField(default=False, verbose_name='Índice de Intensidad Formativa')),
                ('is_using_charlas', models.BooleanField(default=False, verbose_name='Indice de Charlas Periodicas de Seguridad')),
                ('is_using_incidentes', models.BooleanField(default=False, verbose_name='Indice de Reporte de Incidentes')),
                ('is_using_inspecciones', models.BooleanField(default=False, verbose_name='Indice de Inspecciones')),
                ('is_using_observaciones_planeadas', models.BooleanField(default=False, verbose_name='Índice de Observaciones planeadas  de trabajo')),
                ('is_using_auditorias', models.BooleanField(default=False, verbose_name='Índice de Auditorias')),
                ('is_using_simulacros_emergencia', models.BooleanField(default=False, verbose_name='Índice de Simulacros de Emergencia')),
                ('is_using_reconocimiento_trabajador', models.BooleanField(default=False, verbose_name='Índice de Reconocimiento del Trabajador')),
                ('is_using_engenieer', models.BooleanField(default=False, verbose_name='Índice de Disponibilidad Ingeniero SST')),
                ('is_using_first_auxi', models.BooleanField(default=False, verbose_name='Índice de Accidentes con Primeros Auxilios')),
                ('is_using_medic_atention', models.BooleanField(default=False, verbose_name='Índice de Accidentes con Atención Médica')),
                ('is_using_lose_time', models.BooleanField(default=False, verbose_name='Índice de Accidentes con Tiempo Perdido')),
                ('is_using_fatal_accident', models.BooleanField(default=False, verbose_name='Índice de Accidentes Fatales')),
                ('is_using_frecuency', models.BooleanField(default=False, verbose_name='Índice de Frecuencia')),
                ('is_using_severity', models.BooleanField(default=False, verbose_name='Índice de Severidad')),
                ('is_using_accidentality', models.BooleanField(default=False, verbose_name='Índice de Accidentabilidad')),
                ('is_using_professional_sick', models.BooleanField(default=False, verbose_name='Índice de Enfermedades Profesionales')),
                ('is_using_medic_exam', models.BooleanField(default=False, verbose_name='Índice de Examen Médico Ocupacional')),
                ('is_using_ap_worker', models.BooleanField(default=False, verbose_name='Índice de Trabajadores Aptos')),
                ('is_using_ap_worker_restric', models.BooleanField(default=False, verbose_name='Índice de Trabajadores Aptos con restricción')),
                ('is_using_aq_exposition', models.BooleanField(default=False, verbose_name='Índice de Exposición a  Agentes Químicos')),
                ('is_using_monitoring', models.BooleanField(default=False, verbose_name='Índice de Monitoreos Ocupacionales')),
                ('is_using_medidas_control', models.BooleanField(default=False, verbose_name='Índice de Medidas de Control Ocupacional')),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Index_de_charlas',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DE CHARLAS PERIODICAS DE SEGURIDAD', max_length=100)),
                ('num_charlas_programadas', models.IntegerField()),
                ('num_charlas_realizadas', models.IntegerField()),
                ('num_trabajadores_capacitados', models.IntegerField()),
                ('num_trabajadores_programados', models.IntegerField()),
            ],
        ),

        migrations.CreateModel(
            name='Indice_de_Severidad',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DE SEVERIDAD', max_length=100)),
                ('num_accidents', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Indice_disponibilidad_ingeniero_sst',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DISPONIBILIDAD INGENIERO SST', max_length=100)),
                ('num_horas', models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Indice_Frecuencia',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DE FRECUENCIA', max_length=100)),
                ('num_horas', models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Indice_Inspecciones',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DE INSPECCIONES', max_length=100)),
                ('num_inspeccion_obvs_planeada', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Indice_Medico',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DE EXAMEN MEDICO OCUPACIONAL', max_length=100)),
                ('num_examenes', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Indice_reconocimiento_trabajador',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DE RECONOCIMIENTO DEL TRABAJADOR', max_length=100)),
                ('num_trabajadores', models.IntegerField()),
                ('num_reconocidos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Indice_Reporte_Incidente',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INCIDE DE REPORTE DE INCIDENTES', max_length=100)),
                ('num_incidentes_peligrosos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Liderazgo_Participativo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE LIDERAZGO PARTICIPATIVO', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Medida_IPERC',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DE MEDIDAS DE CONTROL IPERC', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Mejoras_Index',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DE MEJORAS', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='No_Conformidades',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE DE NO CONFORMIDADES', max_length=100)),
                ('type', models.IntegerField(default=1, choices=[(1, 'INTERNA'), (2, 'EXTERNA')])),
                ('num_menores', models.IntegerField(blank=True, null=True)),
                ('num_mayores', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan_Contingencia',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='INDICE PLAN DE CONTINGENCIA', max_length=100)),
            ],
        ),
    ]
