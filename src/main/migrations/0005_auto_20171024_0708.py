# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_mediccontrol_program'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountWorker',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(upload_to=main.models.upload_image_to, null=True, verbose_name='Logo', blank=True),
        ),
        migrations.AddField(
            model_name='countworker',
            name='company',
            field=models.ForeignKey(to='main.Company'),
        ),
    ]
