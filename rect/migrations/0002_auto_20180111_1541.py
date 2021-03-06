# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-11 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rect', '0001_auto_20180111_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='page',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, '初始化'), (1, '切分数据未上传'), (3, '字块数据未展开'), (2, '数据解析失败'), (4, '图片不存在'), (5, '列图不存在'), (6, '列图坐标不存在'), (7, '已准备好')], db_index=True, default=0, verbose_name='操作类型'),
        ),
    ]
