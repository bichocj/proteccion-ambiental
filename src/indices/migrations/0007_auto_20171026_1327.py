# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0006_auto_20171024_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuesdetail',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]
