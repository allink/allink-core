# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-07 10:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('allink_content', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkcontentplugin',
            name='overlay_styles_enabled',
        ),
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='inverted_colors_enabled',
            field=models.BooleanField(default=False, help_text='If checked, the predefined inverted text colors are applied (suitable when using a background image/video)', verbose_name='Activate "inverted text colors"'),
        ),
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='overlay_enabled',
            field=models.BooleanField(default=False, help_text='If checked, a predefined overlay background gradient/color is applied (suitable when using a background image/video)', verbose_name='Activate "overlay"'),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='video_poster_image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='This image is displayed while the video is loading. Ideally, use an <strong>exact screen capture image</strong> of the very first frame of the video for best results.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_video_poster_image', to='filer.Image', verbose_name='Video Start Image'),
        ),
    ]
