# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 15:31
from __future__ import unicode_literals

import distances.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('distances', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='time',
        ),
        migrations.AddField(
            model_name='exercise',
            name='hours',
            field=distances.fields.IntegerRangeField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exercise',
            name='minutes',
            field=distances.fields.IntegerRangeField(default=0),
            preserve_default=False,
        ),
    ]
