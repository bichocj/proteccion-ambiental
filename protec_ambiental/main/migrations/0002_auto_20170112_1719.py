# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historyformats',
            old_name='requeriments',
            new_name='requeriment',
        ),
        migrations.AddField(
            model_name='format',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
    ]
