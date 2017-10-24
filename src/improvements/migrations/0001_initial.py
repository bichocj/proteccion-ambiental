# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20171024_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100, verbose_name='Titulo')),
                ('content', models.TextField(verbose_name='description', null=True, blank=True)),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='date')),
                ('is_active', models.BooleanField(default=True)),
                ('percentage', models.DecimalField(decimal_places=2, null=True, max_digits=10, verbose_name='percentage')),
                ('company', models.ForeignKey(to='main.Company', related_name='agreement_company')),
            ],
        ),
        migrations.CreateModel(
            name='AgreementDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(verbose_name='description')),
                ('date_until', models.DateField(null=True, verbose_name='start date')),
                ('date_start', models.DateField(null=True, verbose_name='end date')),
                ('state', models.IntegerField(default=0, choices=[(0, 'to do'), (1, 'following'), (2, 'done')], verbose_name='state')),
                ('evidence', models.FileField(null=True, upload_to='improvements/', verbose_name='evidence')),
                ('agreement', models.ForeignKey(to='improvements.Agreement')),
            ],
        ),
        migrations.CreateModel(
            name='Metting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100, verbose_name='Titulo')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='date')),
                ('percentage', models.DecimalField(decimal_places=2, null=True, max_digits=10, verbose_name='percentage')),
                ('evidence', models.FileField(null=True, upload_to='improvements/meetings/', verbose_name='evidence')),
                ('company', models.ForeignKey(to='main.Company', related_name='metting_company')),
            ],
        ),
        migrations.AddField(
            model_name='agreement',
            name='metting',
            field=models.ForeignKey(null=True, blank=True, to='improvements.Metting'),
        ),
    ]
