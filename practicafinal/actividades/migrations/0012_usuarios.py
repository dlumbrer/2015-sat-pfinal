# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0011_ultimaactualizacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.TextField()),
                ('usuario', models.CharField(max_length=32)),
                ('actividades', models.ManyToManyField(to='actividades.Actividades')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
