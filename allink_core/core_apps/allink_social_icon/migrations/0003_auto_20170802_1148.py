# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-02 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_social_icon', '0002_allinksocialiconcontainerplugin_project_css_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinksocialiconplugin',
            name='icon',
            field=models.CharField(max_length=50, verbose_name='Icon'),
        ),
    ]