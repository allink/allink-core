# -*- coding: utf-8 -*-
# Generated by Django 1.9.13post1 on 2018-11-09 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_gallery', '0004_auto_20181109_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgalleryimageplugin',
            name='template',
            field=models.CharField(help_text='Choose a template.', max_length=50, verbose_name='Template'),
        ),
    ]