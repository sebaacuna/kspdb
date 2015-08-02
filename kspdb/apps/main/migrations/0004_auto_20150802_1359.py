# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_craft_sha'),
    ]

    operations = [
        migrations.AddField(
            model_name='craft',
            name='blob',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='sha',
            field=models.CharField(max_length=40, blank=True, null=True),
        ),
    ]
