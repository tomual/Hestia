# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-13 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0007_auto_20170913_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.CharField(max_length=200),
        ),
    ]
