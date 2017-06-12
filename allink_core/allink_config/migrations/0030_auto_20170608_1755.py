# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0029_allinkmetatagextension_override_h1'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkconfig',
            name='gallery_plugin_caption_text_max_length',
            field=models.IntegerField(verbose_name='Gallery Plugin max length of caption text Field', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='gallery_plugin_caption_text_styling_disabled',
            field=models.BooleanField(verbose_name='Gallery Plugin render output with no styling', default=False),
        ),
    ]
