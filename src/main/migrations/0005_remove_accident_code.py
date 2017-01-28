# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170127_0412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accident',
            name='code',
        ),
    ]
