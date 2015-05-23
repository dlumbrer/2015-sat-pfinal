# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0012_usuarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apuntada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.TextField()),
                ('actividad', models.ForeignKey(to='actividades.Actividades')),
                ('usuario', models.ForeignKey(to='actividades.Usuarios')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='usuarios',
            name='actividades',
        ),
        migrations.AddField(
            model_name='usuarios',
            name='descripcion',
            field=models.TextField(default='Bienvenido a mi pagina de actividades personal :D'),
            preserve_default=False,
        ),
    ]
