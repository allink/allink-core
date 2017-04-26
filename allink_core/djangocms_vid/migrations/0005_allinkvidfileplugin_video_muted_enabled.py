# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_vid', '0004_auto_20170411_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkvidfileplugin',
            name='video_muted_enabled',
            field=models.BooleanField(default=True, help_text='Caution: Autoplaying videos with audio is not recommended. Use wisely.', verbose_name='Muted'),
        ),
    ]
