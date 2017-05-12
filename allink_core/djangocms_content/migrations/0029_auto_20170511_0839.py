# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import filer.fields.file
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0028_auto_20170411_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='bg_image_inner_container',
            field=filer.fields.image.FilerImageField(to='filer.Image', related_name='content_container_bg_image', help_text='Adds a background image to the inner container of a content section. Activating "overlay styles" is recommended.', verbose_name='Background-Image', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='video_file',
            field=filer.fields.file.FilerFileField(to='filer.File', related_name='content_video_file', help_text='Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>File size: Dependent of video length. Generally speaking: Less is more.', verbose_name='Source', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='video_mobile_image',
            field=filer.fields.image.FilerImageField(to='filer.Image', related_name='content_video_mobile_image', help_text='The image that is being displayed instead of the video on mobile devices.', verbose_name='Mobile Image', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='video_mobile_image_alignment',
            field=models.CharField(max_length=50, verbose_name='Mobile Image Alignment (horizontal)', choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], default='center', help_text='Which part of the image ist the most important one and <strong>must</strong> be visible? Because we use the available space, there is a chance that a part (left and/or right) is not visible.'),
        ),
    ]
