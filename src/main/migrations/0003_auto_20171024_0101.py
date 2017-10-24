# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20171023_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(null=True, upload_to=main.models.upload_image_to, blank=True, verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='estado',
            field=models.BooleanField(default=True, verbose_name='Esta activo'),
        ),
    ]
