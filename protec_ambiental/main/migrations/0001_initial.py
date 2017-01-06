# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('ruc', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('time', models.IntegerField()),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('requeriments', models.IntegerField()),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryFormats',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('requeriments', models.IntegerField()),
                ('date_time', models.DateTimeField()),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.DateTimeField()),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('meeting', models.ForeignKey(null=True, to='main.Meeting', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UseProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(to='main.Product')),
                ('task', models.ForeignKey(to='main.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('time', models.DateTimeField()),
                ('employee', models.ForeignKey(to='main.Employee')),
                ('task', models.ForeignKey(to='main.Task')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='company',
            field=models.ForeignKey(to='main.Company'),
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
