# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0025_auto_20170518_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkmetatagextension',
            name='og_description',
            field=models.CharField(max_length=255, blank=True, help_text='Description when shared on Facebook.', null=True, verbose_name='Meta Description for Search Engines and when shared on Facebook.'),
        ),
        migrations.AlterField(
            model_name='allinkmetatagextension',
            name='og_image',
            field=filer.fields.image.FilerImageField(to='filer.Image', null=True, blank=True, help_text='Preview image when page/post is shared on Facebook. <br>Min. 1200 x 630 for best results. If not set, the one from the preview image will be used, if not set or not in a app context, the one defined in allink_settings will be used.', verbose_name='og:Image'),
        ),
        migrations.AlterField(
            model_name='allinkmetatagextension',
            name='og_title',
            field=models.CharField(max_length=255, blank=True, help_text='Title when shared on Facebook.', null=True, verbose_name='Title Tag and Title when shared on Facebook.'),
        ),
    ]
