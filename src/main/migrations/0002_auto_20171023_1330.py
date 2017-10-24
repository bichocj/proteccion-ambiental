# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(upload_to=main.models.upload_image_to, verbose_name='Logo', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historyformats',
            name='date_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
