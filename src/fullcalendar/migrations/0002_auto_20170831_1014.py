# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fullcalendar', '0001_initial'),
        ('main', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='company',
            field=models.ForeignKey(to='main.Company'),
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
