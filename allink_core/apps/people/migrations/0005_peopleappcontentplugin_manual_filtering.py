# -*- coding: utf-8 -*-
# Generated by Django 1.9.13post1 on 2018-05-17 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20170720_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='peopleappcontentplugin',
            name='manual_filtering',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
