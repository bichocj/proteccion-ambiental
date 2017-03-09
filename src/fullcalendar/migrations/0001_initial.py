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
                ('title', models.CharField(verbose_name='Titulo', max_length=200, blank=None)),
                ('slug', models.SlugField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'crear calendario',
                'permissions': (('view_calendars', 'Can see existing calendars'),),
                'verbose_name_plural': 'Calendars',
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
                ('is_cancelled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('calendar', models.ForeignKey(to='fullcalendar.Calendar')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_by_event')),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='type', max_length=200, blank=None)),
            ],
        ),
        migrations.AddField(
            model_name='events',
            name='type',
            field=models.ForeignKey(to='fullcalendar.EventType'),
        ),
    ]
