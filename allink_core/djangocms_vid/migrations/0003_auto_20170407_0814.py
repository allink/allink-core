# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_vid', '0002_auto_20170404_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkvidembedplugin',
            name='ratio',
            field=models.CharField(max_length=50, null=True, verbose_name='Ratio', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkvidembedplugin',
            name='video_service',
            field=models.CharField(max_length=50, choices=[('youtube', 'Youtube'), ('vimeo', 'Vimeo')], verbose_name='Video Service'),
        ),
    ]
