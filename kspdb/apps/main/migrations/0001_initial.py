# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import kspdb.apps.main.models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Craft',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('url', models.URLField(null=True)),
                ('data', models.TextField(null=True)),
                ('name', kspdb.apps.main.models.NameField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('repo', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('sha', models.CharField(max_length=40, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mesh',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('url', models.URLField(null=True)),
                ('data', models.TextField(null=True)),
                ('json', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('url', models.URLField(null=True)),
                ('data', models.TextField(null=True)),
                ('name', kspdb.apps.main.models.NameField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PartCollection',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('repo', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('sha', models.CharField(max_length=40, null=True, blank=True)),
                ('name', kspdb.apps.main.models.NameField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='part',
            name='collection',
            field=models.ForeignKey(to='main.PartCollection'),
        ),
        migrations.AddField(
            model_name='part',
            name='mesh',
            field=models.OneToOneField(to='main.Mesh'),
        ),
        migrations.AddField(
            model_name='craft',
            name='game',
            field=models.ForeignKey(to='main.Game'),
        ),
    ]
