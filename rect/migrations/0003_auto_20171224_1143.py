# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-24 03:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rect', '0002_auto_20171223_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='desc',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='计划格式化描述'),
        ),
    ]