# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('ruc', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('requeriments', models.IntegerField()),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryFormats',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('requeriments', models.IntegerField()),
                ('date_time', models.DateTimeField()),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('date_time', models.DateTimeField()),
                ('type_calendar', models.IntegerField()),
                ('charge', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('expiration', models.DateTimeField()),
                ('company', models.ForeignKey(to='main.Company')),
                ('meeting', models.ForeignKey(to='main.Meeting', blank=True, null=True)),
            ],
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
