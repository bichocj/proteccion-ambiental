# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170131_0630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='accident',
            name='date',
            field=models.DateField(verbose_name='date', default=datetime.datetime(2017, 1, 31, 6, 59, 46, 249732)),
        ),
        migrations.AddField(
            model_name='accident',
            name='evidence',
            field=models.ForeignKey(null=True, to='main.Evidence'),
        ),
    ]
