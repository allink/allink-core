# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0025_auto_20161205_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='video_poster_image',
            field=filer.fields.image.FilerImageField(related_name='content_video_poster_image', blank=True, to='filer.Image', help_text='This image is displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.', null=True, verbose_name='Video Start Image'),
        ),
    ]
