# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-12 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_image', '0003_auto_20170707_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_special',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Special Links'),
        ),
    ]
