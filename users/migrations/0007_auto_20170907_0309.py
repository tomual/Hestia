# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 02:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20170907_0308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='icon',
            field=models.ImageField(default='static/icons/aurora.png', upload_to='static/icons'),
        ),
    ]