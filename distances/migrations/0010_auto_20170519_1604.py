# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 13:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distances', '0009_auto_20170512_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='full name')),
            ],
        ),
        migrations.AlterField(
            model_name='dates',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2017, 5, 12, 16, 4, 30, 207923)),
        ),
    ]
