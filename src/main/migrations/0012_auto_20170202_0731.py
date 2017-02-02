# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20170201_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 2, 2, 7, 31, 22, 626537), verbose_name='date'),
        ),
    ]
