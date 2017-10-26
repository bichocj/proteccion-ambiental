# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0004_auto_20171023_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='valuesdetail',
            name='value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
