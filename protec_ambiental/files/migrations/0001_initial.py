# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('texto', models.TextField(blank=True, null=True)),
                ('archivo', models.FileField(blank=True, null=True, upload_to='archivos/')),
            ],
        ),
    ]
