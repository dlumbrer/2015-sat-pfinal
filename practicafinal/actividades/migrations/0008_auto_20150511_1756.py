# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0007_actividades_latitud'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividades',
            name='latitud',
        ),
        migrations.RemoveField(
            model_name='actividades',
            name='longitud',
        ),
    ]
