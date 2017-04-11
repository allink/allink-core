# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_vid', '0003_auto_20170407_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkvidfileplugin',
            name='video_file_height',
            field=models.IntegerField(blank=True, verbose_name='Video height', null=True),
        ),
        migrations.AddField(
            model_name='allinkvidfileplugin',
            name='video_file_width',
            field=models.IntegerField(blank=True, verbose_name='Video width', null=True),
        ),
    ]
