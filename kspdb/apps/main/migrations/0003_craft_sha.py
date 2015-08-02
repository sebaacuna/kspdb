# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_game_sha'),
    ]

    operations = [
        migrations.AddField(
            model_name='craft',
            name='sha',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
