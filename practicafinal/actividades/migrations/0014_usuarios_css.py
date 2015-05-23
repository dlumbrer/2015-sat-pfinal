# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0013_auto_20150515_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='css',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
