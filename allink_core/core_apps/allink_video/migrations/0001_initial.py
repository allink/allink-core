# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-21 09:32
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import djangocms_attributes_field.fields
import filer.fields.file
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkVideoEmbedPlugin',
            fields=[
                ('attributes', djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, verbose_name='Attributes')),
                ('project_css_classes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_video_allinkvideoembedplugin', serialize=False, to='cms.CMSPlugin')),
                ('video_id', models.CharField(help_text='Only provide the ID. The correct URL will automatically be generated.<br><br>YouTube: https://www.youtube.com/watch?v=<strong>12345678</strong> (the ID is <strong>12345678</strong>)<br>Vimeo: https://vimeo.com/<strong>12345678</strong> (the ID is <strong>12345678</strong>)', max_length=255, verbose_name='Video ID')),
                ('video_service', models.CharField(choices=[('youtube', 'Youtube'), ('vimeo', 'Vimeo')], max_length=50, verbose_name='Video Service')),
                ('ratio', models.CharField(blank=True, max_length=50, null=True, verbose_name='Ratio')),
                ('auto_start_enabled', models.BooleanField(default=False, help_text='<strong>Important:</strong> Autoplaying videos with audio is not recommended. Use wisely. ', verbose_name='Autostart')),
                ('allow_fullscreen_enabled', models.BooleanField(default=True, verbose_name='Allow fullscreen')),
            ],
            options={
                'verbose_name': 'Allink Video Embed',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='AllinkVideoFilePlugin',
            fields=[
                ('attributes', djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, verbose_name='Attributes')),
                ('project_css_classes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_video_allinkvideofileplugin', serialize=False, to='cms.CMSPlugin')),
                ('video_file_width', models.IntegerField(blank=True, null=True, verbose_name='Video width')),
                ('video_file_height', models.IntegerField(blank=True, null=True, verbose_name='Video height')),
                ('video_muted_enabled', models.BooleanField(default=True, help_text='Caution: Autoplaying videos with audio is not recommended. Use wisely.', verbose_name='Muted')),
                ('poster_only_on_mobile', models.BooleanField(default=True, help_text='Disable video on mobile devices and only show the start image without video control.', verbose_name='Image Only (Mobile)')),
                ('auto_start_enabled', models.BooleanField(default=True, verbose_name='Autostart')),
                ('allow_fullscreen_enabled', models.BooleanField(default=False, verbose_name='Allow fullscreen')),
                ('video_file', filer.fields.file.FilerFileField(help_text='Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>File size: Dependent of video length. Generally speaking: Less is more.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='allink_video_allinkvideofileplugin_video_file', to='filer.File', verbose_name='Video File')),
                ('video_poster_image', filer.fields.image.FilerImageField(help_text='Image that is being displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.<br><br><strong>Imoprtant:</strong> Make sure the aspect ratio of the image is <strong>exactly the same</strong> as the video, otherwise the video height will shrink or grow when the playback starts.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allink_video_allinkvideofileplugin_video_poster_image', to='filer.Image', verbose_name='Video Start Image')),
            ],
            options={
                'verbose_name': 'Allink Video File',
            },
            bases=('cms.cmsplugin',),
        ),
    ]