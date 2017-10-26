# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0008_auto_20171026_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuesdetail',
            name='denominator',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='valuesdetail',
            name='numerator',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
