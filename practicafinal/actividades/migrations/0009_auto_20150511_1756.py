# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0008_auto_20150511_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividades',
            name='lat',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='actividades',
            name='lon',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
