# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
        ('fullcalendar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='company',
            field=models.ForeignKey(to='main.Company', related_name='company'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_by'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='users',
            field=models.ManyToManyField(verbose_name='shared with', to=settings.AUTH_USER_MODEL, related_name='users'),
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
