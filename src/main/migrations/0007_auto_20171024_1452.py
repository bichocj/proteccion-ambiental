# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20171024_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countworker',
            name='quantity',
            field=models.IntegerField(verbose_name='cantidad de trabajadores'),
        ),
    ]
