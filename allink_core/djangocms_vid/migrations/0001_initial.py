# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import filer.fields.image
import django.db.models.deletion
import django.contrib.postgres.fields
import djangocms_attributes_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0007_auto_20161016_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkVidEmbedPlugin',
            fields=[
                ('auto_start_enabled', models.BooleanField(default=True, verbose_name='Autostart')),
                ('attributes', djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True)),
                ('project_css_classes', django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(max_length=50, null=True, blank=True), blank=True)),
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_vid_allinkvidembedplugin', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('video_id', models.CharField(help_text='Only provide the ID. The correct url will be automatically generated.', max_length=255, verbose_name='Video ID')),
                ('video_service', models.CharField(max_length=50, verbose_name='Video Service', choices=[(b'youtube', 'Youtube'), (b'vimeo', 'Vimeo')])),
                ('ratio', models.CharField(blank=True, max_length=50, null=True, verbose_name='Ratio', choices=[(b'3-2', b'3:2'), (b'2-1', b'2:1'), (b'4-3', b'4:3'), (b'1-1', b'1:1'), (b'16-9', b'16:9'), (b'x-y', b'Original')])),
                ('video_poster_image', filer.fields.image.FilerImageField(related_name='djangocms_vid_allinkvidembedplugin_video_poster_image', blank=True, to='filer.Image', help_text='This image is displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.', null=True, verbose_name='Video Start Image')),
            ],
            options={
                'verbose_name': 'Allink Video Embed',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='AllinkVidFilePlugin',
            fields=[
                ('auto_start_enabled', models.BooleanField(default=True, verbose_name='Autostart')),
                ('attributes', djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True)),
                ('project_css_classes', django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(max_length=50, null=True, blank=True), blank=True)),
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_vid_allinkvidfileplugin', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('video_file', filer.fields.file.FilerFileField(related_name='djangocms_vid_allinkvidfileplugin_video_file', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Video File', to='filer.File', help_text='Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>Aspect ratio: TBD<br>File size: Dependent of video length. Generally speaking: Less is more.', null=True)),
                ('video_poster_image', filer.fields.image.FilerImageField(related_name='djangocms_vid_allinkvidfileplugin_video_poster_image', blank=True, to='filer.Image', help_text='This image is displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.', null=True, verbose_name='Video Start Image')),
            ],
            options={
                'verbose_name': 'Allink Video File',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
