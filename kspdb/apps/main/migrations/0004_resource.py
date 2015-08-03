# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kspdb.apps.main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_part_partname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', kspdb.apps.main.models.NameField(unique=True, max_length=255)),
                ('density', models.FloatField(default=0)),
                ('unitCost', models.FloatField(default=0)),
                ('flowMode', models.CharField(choices=[('ALL_VESSEL', 'ALL_VESSEL'), ('NO_FLOW', 'NO_FLOW'), ('STACK_PRIORITY_SEARCH', 'STACK_PRIORITY_SEARCH'), ('STAGE_PRIORITY_FLOW', 'STAGE_PRIORITY_FLOW')], max_length=50)),
                ('transfer', models.CharField(default='NONE', max_length=10)),
                ('hsp', models.IntegerField(default=0)),
            ],
        ),
    ]
