# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170816_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='icon',
            field=models.ImageField(blank=True, upload_to='static/icons'),
        ),
    ]
