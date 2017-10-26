# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0005_valuesdetail_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuesdetail',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
