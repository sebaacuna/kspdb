# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='mesh',
            field=models.OneToOneField(to='main.Mesh', null=True),
        ),
    ]
