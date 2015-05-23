# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_auto_20150510_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actividades',
            old_name='localidad',
            new_name='lugar',
        ),
        migrations.RemoveField(
            model_name='actividades',
            name='provincia',
        ),
        migrations.AlterField(
            model_name='actividades',
            name='precio',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
