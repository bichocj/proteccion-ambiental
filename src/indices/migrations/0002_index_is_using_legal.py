# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='index',
            name='is_using_legal',
            field=models.BooleanField(verbose_name='Índice Legal', default=False),
        ),
    ]
