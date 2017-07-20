# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-20 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20170710_1012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locations',
            name='is_active',
        ),
        migrations.AddField(
            model_name='locations',
            name='status',
            field=models.IntegerField(choices=[(1, 'active'), (2, 'inactive')], default=1, verbose_name='status'),
        ),
    ]
