# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20170128_2207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historyformats',
            old_name='document',
            new_name='file',
        ),
    ]
