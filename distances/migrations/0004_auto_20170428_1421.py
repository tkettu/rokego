# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 11:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('distances', '0003_auto_20170425_1354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercise',
            options={'verbose_name_plural': 'exercises'},
        ),
        migrations.AddField(
            model_name='exercise',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
