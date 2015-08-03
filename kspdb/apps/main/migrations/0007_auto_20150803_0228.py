# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150803_0142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('url', models.URLField(null=True)),
                ('data', models.TextField(null=True)),
                ('path', models.TextField(null=True)),
                ('geometry', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='part',
            name='mesh',
        ),
        migrations.DeleteModel(
            name='Mesh',
        ),
        migrations.AddField(
            model_name='part',
            name='mu',
            field=models.OneToOneField(null=True, to='main.Mu'),
        ),
    ]
