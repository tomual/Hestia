# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20170907_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='icon',
            field=models.ImageField(default='static/group_icons/aurora2.jpg', upload_to='static/group_icons'),
        ),
    ]
