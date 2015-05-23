# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0010_actividades_masinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='UltimaActualizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ultima', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
