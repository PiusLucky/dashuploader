# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-01 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeginningDash', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsbyadmin',
            name='News',
            field=models.TextField(default='', max_length=10000),
        ),
    ]
