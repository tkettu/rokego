# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-14 11:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distances', '0020_auto_20170709_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dates',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2017, 7, 7, 11, 41, 55, 410218)),
        ),
    ]
