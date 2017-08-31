# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0002_index_is_using_legal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index_Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('mounth', models.IntegerField(blank=True, null=True)),
                ('sgsst', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('legal', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('icsst', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('indice_no_conformidad', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('medida_iperc', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('liderazgo', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('plan_contingencia', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('mejora', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('capacitacion', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('personal_capacitado', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('intensidad_formativa', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('charlas', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('incidentes', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('inspecciones', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('observaciones_planeadas', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('auditorias', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('simulacros_emergencia', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('reconocimiento_trabajador', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('engenieer', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('first_auxi', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('medic_atention', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('lose_time', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('fatal_accident', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('frecuency', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('severity', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('accidentality', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('professional_sick', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('medic_exam', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('ap_worker', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('ap_worker_restric', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('exposition', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('monitoring', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('medidas_control', models.DecimalField(default=True, null=True, decimal_places=2, max_digits=10)),
                ('index', models.ForeignKey(to='indices.Index')),
            ],
        ),
        migrations.CreateModel(
            name='ValuesDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('key', models.CharField(blank=True, max_length=100, null=True)),
                ('numerator', models.IntegerField(blank=True, null=True)),
                ('denominator', models.IntegerField(blank=True, null=True)),
                ('detail', models.ForeignKey(to='indices.Index_Detail')),
            ],
        ),
    ]
