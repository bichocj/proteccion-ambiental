# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    operations = [
        migrations.CreateModel(
            name='Accessibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=None, max_length=200, verbose_name='title')),
                ('slug', models.SlugField(max_length=100)),
                ('min_time', models.TimeField(null=True, blank=True, verbose_name='min time')),
                ('max_time', models.TimeField(null=True, blank=True, verbose_name='max time')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='assigned to', null=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_by')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='users', verbose_name='shared with')),
            ],
            options={
                'verbose_name': 'Calendar',
                'permissions': (('view_calendars', 'Can see existing calendars'),),
                'verbose_name_plural': 'Calendars',
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
        migrations.AddField(
            model_name='accessibility',
            name='calendar',
            field=models.ForeignKey(to='fullcalendar.Calendar'),
        ),
        migrations.AddField(
            model_name='accessibility',
            name='group',
            field=models.ForeignKey(to='auth.Group'),
        ),
    ]
