# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-16 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='telphone',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='user',
            name='telphone',
            field=models.CharField(max_length=11, verbose_name='手机号码'),
        ),
    ]
