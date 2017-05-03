# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_vid', '0005_allinkvidfileplugin_video_muted_enabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkvidembedplugin',
            name='video_poster_image',
        ),
        migrations.AddField(
            model_name='allinkvidfileplugin',
            name='poster_only_on_mobile',
            field=models.BooleanField(default=True, verbose_name='Poster Only (Mobile)', help_text='Disable video on mobile devices and only show the start image without video control.'),
        ),
        migrations.AlterField(
            model_name='allinkvidembedplugin',
            name='allow_fullscreen_enabled',
            field=models.BooleanField(default=True, verbose_name='Allow fullscreen'),
        ),
        migrations.AlterField(
            model_name='allinkvidembedplugin',
            name='video_id',
            field=models.CharField(max_length=255, verbose_name='Video ID', help_text='Only provide the ID. The correct URL will automatically be generated.<br><br>YouTube: https://www.youtube.com/watch?v=12345678 (the ID is <strong>12345678</strong>)<br>Vimeo: https://vimeo.com/12345678 (the ID is <strong>12345678</strong>)'),
        ),
        migrations.AlterField(
            model_name='allinkvidfileplugin',
            name='video_poster_image',
            field=filer.fields.image.FilerImageField(related_name='djangocms_vid_allinkvidfileplugin_video_poster_image', verbose_name='Video Start Image', null=True, to='filer.Image', help_text='This image is displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.'),
        ),
    ]
