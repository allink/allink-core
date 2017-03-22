# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_group', '0002_auto_20170321_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgroupcontainerplugin',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='allinkgroupplugin',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
    ]
