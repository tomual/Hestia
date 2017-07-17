# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 00:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_content', models.CharField(max_length=200)),
                ('reply_date', models.DateTimeField(verbose_name='date posted')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread_title', models.CharField(max_length=200)),
                ('thread_content', models.CharField(max_length=200)),
                ('thread_date', models.DateTimeField(verbose_name='date posted')),
            ],
        ),
        migrations.AddField(
            model_name='response',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forums.Thread'),
        ),
    ]
