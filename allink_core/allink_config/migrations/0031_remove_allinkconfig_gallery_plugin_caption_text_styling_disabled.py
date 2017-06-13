# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0030_auto_20170608_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkconfig',
            name='gallery_plugin_caption_text_styling_disabled',
        ),
    ]
