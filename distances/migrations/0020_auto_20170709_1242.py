# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-09 12:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distances', '0019_auto_20170709_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dates',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2017, 7, 2, 12, 42, 9, 816676)),
        ),
    ]
