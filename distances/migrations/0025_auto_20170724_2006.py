# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-24 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distances', '0024_remove_exercise_testtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='sport',
            field=models.CharField(choices=[('Running', 'Running'), ('Skiing', 'Skiing'), ('Walking', 'Walking'), ('Cycling', 'Cycling'), ('Swimming', 'Swimming'), ('Rowing', 'Rowing'), ('Other', 'Other')], default='Running', max_length=20),
        ),
    ]
