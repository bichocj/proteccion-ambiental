# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import datetime
from django.conf import settings
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Titulo')),
                ('content', models.TextField(null=True, verbose_name='Descripcion', blank=True)),
                ('type_accident', models.IntegerField(choices=[(1, 'ACCIDENTES CON PRIMEROS AUXILIOS'), (2, 'ACCCIDENTE CON ATENCION MEDICA'), (3, 'ACCIDENTES CON TIEMPO PERDIDO'), (4, 'ACCIDENTES FATALES'), (5, 'INCIDENTES PELIGROS'), (6, 'ENFERMEDADES OCUPACIONALES'), (7, 'ACTOS INSEGUROS')], default=1, verbose_name='Tipo de Accidente')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha')),
                ('lose_days', models.DecimalField(max_digits=5, null=True, verbose_name='Dias Perdidos', blank=True, decimal_places=2)),
                ('evidence', models.FileField(null=True, verbose_name='Evidencia', upload_to='accident/')),
            ],
        ),
        migrations.CreateModel(
            name='AccidentDetail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('accident', models.ForeignKey(to='main.Accident')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ruc', models.IntegerField(unique=True, verbose_name='R.U.C.')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre Compañia')),
                ('short_name', models.CharField(max_length=100, unique=True, verbose_name='Nombre Corto')),
                ('slug', models.SlugField(max_length=100, null=True, unique=True, blank=True, verbose_name='slug')),
                ('logo', models.ImageField(upload_to=main.models.upload_image_to, null=True, verbose_name='Logo', blank=True)),
                ('address', models.CharField(max_length=200, null=True, verbose_name='Dirección', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company_Requirement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user_ptr', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL, auto_created=True, parent_link=True)),
                ('code', models.CharField(max_length=50, verbose_name='Codigo')),
                ('time', models.IntegerField(default=0)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('filename', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('file', models.FileField(upload_to='formatos/', verbose_name='Archivo')),
                ('type_format', models.IntegerField(choices=[(1, 'Planes, Programas y Procedimientos'), (2, 'Registros y Evidencias')], null=True, default=1, verbose_name='Tipo')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('company', models.ForeignKey(null=True, blank=True, to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryFormats',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='history/%Y/%m/%d', blank=True)),
                ('date_time', models.DateTimeField(default=datetime.datetime(2017, 8, 31, 10, 14, 23, 422865))),
                ('format', models.ForeignKey(null=True, blank=True, to='main.Format')),
            ],
        ),
        migrations.CreateModel(
            name='LegalRequirement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('type_normativa', models.CharField(max_length=200, null=True, verbose_name='Tipo Normativa', blank=True)),
                ('normativa', models.CharField(max_length=200, verbose_name='Codigo Normativa')),
                ('datepublication', models.DateField(default=datetime.datetime.now, verbose_name='Fecha Publicacion')),
                ('title', models.CharField(max_length=200, verbose_name='Titulo del Dispositivo Legal')),
                ('apply', models.TextField(verbose_name='Que Aplica?')),
                ('actual_month', models.CharField(max_length=100)),
                ('evidence', models.FileField(null=True, verbose_name='Evidencia Registro', upload_to='legal_requirement/')),
                ('frecuency', models.CharField(max_length=200, null=True, verbose_name='Frecuencia', blank=True)),
                ('date_last_evaluation', models.DateField(null=True, verbose_name='Fecha Ultima Evaluacion', blank=True)),
                ('responsable', models.CharField(max_length=200, null=True, blank=True)),
                ('cumplimiento', models.DecimalField(max_digits=10, null=True, verbose_name='Cumplimiento (%)', blank=True, decimal_places=2)),
                ('observations', models.TextField(null=True, verbose_name='Observaciones', blank=True)),
                ('type_register', models.IntegerField(choices=[(0, 'Generales'), (1, 'Seguridad Ocupacional'), (2, 'Salud Ocupacional'), (3, 'Ergonomia'), (4, 'Mujer Gestante / Personas con limitaciones'), (5, 'Agentes Quimicos / Tabaco'), (6, 'Cancer'), (7, 'Hostigamiento / Disciminacion / VIH - SIDA'), (8, 'Edificacion'), (9, 'Emergencia'), (10, 'Inspeccion en el Trabajo'), (11, 'Electricidad'), (12, 'NTP'), (13, 'Radiaciones'), (14, 'Sanitarias / Alimentacion'), (15, 'Transporte'), (16, 'Normas Tecnicas Internacionales / NFPA / Otros')], default=0, verbose_name='Estado')),
                ('state', models.IntegerField(choices=[(0, 'CUMPLIO'), (1, 'NO CUMPLIO')], default=1, verbose_name='Estado')),
                ('entitie', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='MedicControl',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'APTO'), (1, 'APTO CON RESTRICCION'), (2, 'NO APTO')], default=2, verbose_name='Estado')),
                # ('program', models.IntegerField(choices=[(0, 'CONSERVACION AUDITIVA'), (1, 'CALIDAD DE VIDA'), (2, 'PROMOCION Y PRESERVACION SALUD VISUAL'), (3, 'PROTECCION A LA MUJER GESTANTE Y EN EDAD FERTIL'), (4, 'PROTECCION RESPIRATORIA'), (5, 'VIGILANCIA CONTRA TME'), (6, 'PROTECCION RADIACION UV'), (7, 'RIESGO GEOLOGICO')], default=0, verbose_name='Programa')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='Fecha')),
                ('evidence', models.FileField(null=True, verbose_name='Evidencia', upload_to='examen_medico/')),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre Requerimiento')),
                ('description', models.CharField(max_length=200, null=True, verbose_name='Descripcion', blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('type_requirement', models.IntegerField(choices=[(0, 0), (1, 1)], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('date_time', models.DateTimeField()),
                ('type_calendar', models.IntegerField()),
                ('charge', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('expiration', models.DateTimeField()),
                ('company', models.ForeignKey(to='main.Company')),
                ('meeting', models.ForeignKey(null=True, blank=True, to='main.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='UseProduct',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(to='main.Product')),
                ('task', models.ForeignKey(to='main.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('employee', models.ForeignKey(to='main.Employee')),
                ('task', models.ForeignKey(to='main.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombres')),
                ('last_name', models.CharField(max_length=100, null=True, default='', verbose_name='Apellidos', blank=True)),
                ('code', models.CharField(max_length=100, verbose_name='Codigo')),
                ('cargo', models.IntegerField(choices=[(0, 'GERENTE'), (1, 'SUPERVISOR'), (2, 'ASESOR EXTERNO'), (3, 'RECURSOS HUMANOS'), (4, 'COMITE')], default=3, verbose_name='Cargo')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.AddField(
            model_name='mediccontrol',
            name='worker',
            field=models.ForeignKey(to='main.Worker'),
        ),
        migrations.AddField(
            model_name='format',
            name='requirement',
            field=models.ForeignKey(to='main.Requirement'),
        ),
        migrations.AddField(
            model_name='company_requirement',
            name='requirement',
            field=models.ForeignKey(to='main.Requirement'),
        ),
        migrations.AddField(
            model_name='accidentdetail',
            name='worker',
            field=models.ForeignKey(to='main.Worker'),
        ),
        migrations.AddField(
            model_name='accident',
            name='company',
            field=models.ForeignKey(to='main.Company'),
        ),
        migrations.AddField(
            model_name='accident',
            name='worker',
            field=models.ForeignKey(default=None, to='main.Worker'),
        ),
    ]
