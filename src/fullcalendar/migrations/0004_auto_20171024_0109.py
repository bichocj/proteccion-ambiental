# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fullcalendar', '0003_auto_20171023_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='company',
            field=models.ForeignKey(to='main.Company'),
        ),
    ]
