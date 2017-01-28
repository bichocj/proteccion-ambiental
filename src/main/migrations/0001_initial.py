# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):


    operations = [
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(null=True, blank=True)),
                ('type_accident', models.CharField(null=True, default='HIGH_WORK', choices=[('HIGH_WORK', 'HIGH_WORK'), ('INTOXICATION', 'INTOXICATION')], verbose_name='type accident', max_length=2)),
                ('date', models.DateField(verbose_name='date')),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruc', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(null=True, blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, auto_created=True, parent_link=True, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('time', models.IntegerField()),
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
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='formatos/%Y/%m/%d')),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryFormats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(null=True, blank=True, upload_to='history/%Y/%m/%d')),
                ('date_time', models.DateTimeField()),
                ('format', models.ForeignKey(null=True, to='main.Format', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('title', models.CharField(null=True, blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(null=True, blank=True, max_length=100)),
                ('content', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(null=True, blank=True, max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(null=True, blank=True, max_length=100)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(to='main.Product')),
                ('task', models.ForeignKey(to='main.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            model_name='calendar',
            name='company',
            field=models.ForeignKey(to='main.Company'),
        ),
        migrations.AddField(
            model_name='accident',
            name='company',
            field=models.ForeignKey(to='main.Company'),
        ),
    ]
