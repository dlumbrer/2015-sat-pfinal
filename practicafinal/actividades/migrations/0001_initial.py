# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.TextField()),
                ('tipo', models.TextField()),
                ('precio', models.IntegerField()),
                ('anno', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('dia', models.IntegerField()),
                ('hora', models.TextField()),
                ('duracion', models.TextField()),
                ('url', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
