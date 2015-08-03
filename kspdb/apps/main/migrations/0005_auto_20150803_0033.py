# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def resources(apps, schema_editor):
    resource_class = apps.get_model('main', 'Resource')

    for data in initial_resources:
        res = resource_class(**data)
        try:
            res.save()
        except:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_resource'),
    ]

    operations = [
        migrations.RunPython(resources),
    ]


initial_resources = [
    {
        'name': 'LiquidFuel',
        'density': 0.005,
        'unitCost': 0.8,
        'hsp': 2010,
        'flowMode': 'STACK_PRIORITY_SEARCH',
        'transfer': 'PUMP',
    },
    {
        'name': 'Oxidizer',
        'density': 0.005,
        'unitCost': 0.18,
        'hsp': 1551,
        'flowMode': 'STACK_PRIORITY_SEARCH',
        'transfer': 'PUMP',
    },
    {
        'name': 'SolidFuel',
        'density': 0.0075,
        'unitCost': 0.6,
        'hsp': 920,
        'flowMode': 'NO_FLOW',
        'transfer': 'NONE',
    },
    {
        'name': 'MonoPropellant',
        'density': 0.004,
        'unitCost': 1.2,
        'hsp': 3000,
        'flowMode': 'STAGE_PRIORITY_FLOW',
        'transfer': 'PUMP',
    },
    {
        'name': 'XenonGas',
        'density': 0.0001,
        'unitCost': 4,
        'hsp': 120,
        'flowMode': 'STAGE_PRIORITY_FLOW',
        'transfer': 'PUMP',
    },
    {
        'name': 'ElectricCharge',
        'density': 0,
        'unitCost': 0,
        'hsp': 0,
        'flowMode': 'ALL_VESSEL',
        'transfer': 'PUMP',
    },
    {
        'name': 'IntakeAir',
        'density': 0.005,
        'unitCost': 0,
        'hsp': 10,
        'flowMode': 'ALL_VESSEL',
        'transfer': 'PUMP',
    },
    {
        'name': 'EVA Propellant',
        'density': 0,
        'unitCost': 0,
        'hsp': 3000,
        'flowMode': 'NO_FLOW',
        'transfer': 'PUMP',
    },
    {
        'name': 'Ore',
        'density': 0.010,
        'unitCost': 0.02,
        'flowMode': 'ALL_VESSEL',
        'transfer': 'PUMP',
        'hsp': 1000,
    },
    {
        'name': 'Ablator',
        'density': 0.001,
        'hsp': 400,
        'flowMode': 'NO_FLOW',
        'transfer': 'NONE',
        'unitCost': 0.5,
    },
]
