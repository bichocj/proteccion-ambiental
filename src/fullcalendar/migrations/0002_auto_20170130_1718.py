# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('fullcalendar', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendar',
            options={'verbose_name': 'crear calendario', 'verbose_name_plural': 'Calendars', 'permissions': (('view_calendars', 'Can see existing calendars'),)},
        ),
        migrations.AlterField(
            model_name='calendar',
            name='assigned',
            field=models.ForeignKey(verbose_name='asignado a', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='max_time',
            field=models.TimeField(null=True, verbose_name='until hour', blank=True),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='min_time',
            field=models.TimeField(null=True, verbose_name='since hour', blank=True),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Titulo', blank=None),
        ),
    ]
