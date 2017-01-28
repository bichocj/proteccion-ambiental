# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_accident_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='format',
            old_name='document',
            new_name='file',
        ),
    ]
