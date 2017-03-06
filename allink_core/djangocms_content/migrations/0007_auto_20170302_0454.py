# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0006_auto_20170125_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='video_mobile_image',
            field=filer.fields.image.FilerImageField(related_name='content_video_mobile_image', blank=True, to='filer.Image', help_text='The image being displayed on mobile devices. Dimensions TBD', null=True, verbose_name='Mobile Image'),
        ),
    ]
