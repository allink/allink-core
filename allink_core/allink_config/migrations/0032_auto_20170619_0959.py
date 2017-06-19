# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0031_remove_allinkconfig_gallery_plugin_caption_text_styling_disabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkmetatagextension',
            name='enable_base_title',
        ),
        migrations.AddField(
            model_name='allinkmetatagextension',
            name='disable_base_title',
            field=models.BooleanField(default=False, help_text='If disabled, only the page title will be shown. Everything behind and including the "|" will be removed.', verbose_name='Disable base title'),
        ),
    ]
