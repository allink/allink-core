# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_vid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkvidembedplugin',
            name='allow_fullscreen_enabled',
            field=models.BooleanField(default=False, verbose_name='Allow fullscreen'),
        ),
        migrations.AddField(
            model_name='allinkvidfileplugin',
            name='allow_fullscreen_enabled',
            field=models.BooleanField(default=False, verbose_name='Allow fullscreen'),
        ),
    ]
