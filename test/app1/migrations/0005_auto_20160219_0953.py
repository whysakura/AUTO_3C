# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-19 01:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_car_default_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_mark',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.Mark'),
        ),
    ]
