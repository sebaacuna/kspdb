# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150803_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='mu',
            name='bytedata',
            field=models.BinaryField(default=None),
            preserve_default=False,
        ),
    ]
