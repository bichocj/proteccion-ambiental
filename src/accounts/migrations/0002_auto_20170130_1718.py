# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='sex',
            field=models.IntegerField(default=0, verbose_name='sexo', choices=[(0, 'masculino'), (1, 'femenino')]),
        ),
    ]
