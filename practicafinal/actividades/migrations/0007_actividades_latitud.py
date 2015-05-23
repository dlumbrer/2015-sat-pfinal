# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0006_remove_actividades_latitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividades',
            name='latitud',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
