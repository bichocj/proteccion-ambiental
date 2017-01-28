# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True, parent_link=True, auto_created=True)),
                ('dni', models.IntegerField(null=True, blank=True)),
                ('sex', models.IntegerField(default=0, choices=[(0, 'man'), (1, 'woman')], verbose_name='sex')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
