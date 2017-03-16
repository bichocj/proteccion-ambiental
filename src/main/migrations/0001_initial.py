# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(null=True, blank=True)),
                ('type_accident', models.IntegerField(verbose_name='type accident', choices=[(1, 'ACCIDENT'), (2, 'INCIDENT')], default=1)),
                ('date', models.DateField(verbose_name='date', default=datetime.datetime(2017, 3, 8, 10, 5, 56, 804936))),
                ('evidence', models.FileField(null=True, verbose_name='evidence', upload_to='accident/')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ruc', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True, null=True, verbose_name='slug', blank=True)),
                ('address', models.CharField(null=True, max_length=200, blank=True)),
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
                ('user_ptr', models.OneToOneField(parent_link=True, serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True, auto_created=True)),
                ('code', models.CharField(max_length=50)),
                ('time', models.IntegerField(default=0)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
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
            name ='Format',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('file', models.FileField(upload_to='formatos/')),
                ('type_format', models.IntegerField(null=True, choices=[(1, 'PLANES'), (2, 'REGISTERS')], default=1)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryFormats',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='history/%Y/%m/%d', blank=True)),
                ('date_time', models.DateTimeField()),
                ('format', models.ForeignKey(null=True, to='main.Format', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('title', models.CharField(null=True, max_length=100, blank=True)),
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
                ('title', models.CharField(null=True, max_length=100, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(null=True, max_length=50, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('type_requirement', models.IntegerField(choices=[(0, 0), (1, 1)], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(null=True, max_length=100, blank=True)),
                ('date_time', models.DateTimeField()),
                ('type_calendar', models.IntegerField()),
                ('charge', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('expiration', models.DateTimeField()),
                ('company', models.ForeignKey(to='main.Company')),
                ('meeting', models.ForeignKey(null=True, to='main.Meeting', blank=True)),
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
            model_name='accident',
            name='company',
            field=models.ForeignKey(to='main.Company'),
        ),
    ]
