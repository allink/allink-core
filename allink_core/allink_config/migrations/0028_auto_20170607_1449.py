# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0027_auto_20170607_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkmetatagextension',
            name='enable_base_title',
            field=models.BooleanField(verbose_name='Enable base title', default=True, help_text='If dsiabled, only the page title will be shown. Everything behind and including the "|" will be removed.'),
        ),
        migrations.AlterField(
            model_name='allinkmetatagextension',
            name='og_image',
            field=filer.fields.image.FilerImageField(to='filer.Image', null=True, verbose_name='og:Image', blank=True, help_text='Preview image when page/post is shared on Facebook/ Twitter. <br>Min. 1200 x 630 for best results. If not set, the one from the preview image will be used, if not set or not in a app context, the one defined in allink_settings will be used.'),
        ),
    ]
