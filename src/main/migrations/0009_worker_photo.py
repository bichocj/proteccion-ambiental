# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-02 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20171026_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='photo',
            field=models.ImageField(null=True, upload_to='photos', verbose_name='photo'),
        ),
    ]
