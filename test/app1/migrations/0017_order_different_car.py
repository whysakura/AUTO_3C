# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-26 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_auto_20160225_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='different_car',
            field=models.CharField(default='0', max_length=40),
        ),
    ]