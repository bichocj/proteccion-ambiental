# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0003_index_detail_valuesdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='index_detail',
            name='accidentality',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='ap_worker',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='ap_worker_restric',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='auditorias',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='capacitacion',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='charlas',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='engenieer',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='exposition',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='fatal_accident',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='first_auxi',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='frecuency',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='icsst',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='incidentes',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='indice_no_conformidad',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='inspecciones',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='intensidad_formativa',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='legal',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='liderazgo',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='lose_time',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='medic_atention',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='medic_exam',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='medida_iperc',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='medidas_control',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='mejora',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='monitoring',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='observaciones_planeadas',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='personal_capacitado',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='plan_contingencia',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='professional_sick',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='reconocimiento_trabajador',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='severity',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='sgsst',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='index_detail',
            name='simulacros_emergencia',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0),
        ),
    ]
