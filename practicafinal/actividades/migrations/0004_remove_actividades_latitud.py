# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0003_auto_20150511_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividades',
            name='latitud',
        ),
    ]
