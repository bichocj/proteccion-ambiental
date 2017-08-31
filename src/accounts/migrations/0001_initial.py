# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user_ptr', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL, auto_created=True, parent_link=True)),
                ('dni', models.IntegerField(null=True, blank=True)),
                ('sex', models.IntegerField(choices=[(0, 'masculino'), (1, 'femenino')], default=0, verbose_name='sexo')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
