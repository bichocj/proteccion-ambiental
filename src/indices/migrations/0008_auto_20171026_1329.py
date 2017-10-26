# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0007_auto_20171026_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuesdetail',
            name='value',
            field=models.DecimalField(default=0, max_digits=10, null=True, decimal_places=2),
        ),
    ]
