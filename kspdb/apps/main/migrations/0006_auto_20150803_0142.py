# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150803_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='craft',
            name='path',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='mesh',
            name='path',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='path',
            field=models.TextField(null=True),
        ),
    ]
