# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import filer.fields.file
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0006_auto_20160623_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkContentColumnPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_content_allinkcontentcolumnplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='AllinkContentPlugin',
            fields=[
                ('title', models.CharField(help_text='The section title', max_length=255, null=True, verbose_name='Title', blank=True)),
                ('title_size', models.CharField(default=b'h1', max_length=50, verbose_name='Section Title Size', choices=[(b'h1', 'Title Large'), (b'h2', 'Title Medium')])),
                ('container_enabled', models.BooleanField(default=True, help_text='If checked, an inner container with a maximum width is added', verbose_name='Activate "container"')),
                ('bg_color', models.IntegerField(null=True, verbose_name='Set a predefined background color', blank=True)),
                ('extra_css_classes', models.CharField(help_text='Only use this field if you know what your doing:<br>SPACE separated class names. Only valid CSS class names will work.', max_length=255, null=True, verbose_name='Additional CSS Classes for content-section', blank=True)),
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_content_allinkcontentplugin', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('template', models.CharField(default=(b'col-1', b'1 Column'), help_text='Choose a template.', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-1-2', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')])),
                ('overlay_styles_enabled', models.BooleanField(default=False, help_text='If checked, the predefined overlay styles are applied (suitable when text is over an image/video)', verbose_name='Activate overlay styles')),
                ('full_height_enabled', models.BooleanField(default=False, help_text="If checked, the section will use the available height of the device's/browser's screen.", verbose_name='Activate "full height" mode')),
                ('parallax_enabled', models.BooleanField(default=False, help_text='If checked, the parallax effect is enabled.', verbose_name='Activate Parallax effect')),
                ('video_mobile_image_alignment', models.CharField(default=b'center', help_text='TBD Define which part of the image must be visible. Because we use the available space, there is a chance that a part (left and/or right) is not visible.', max_length=50, verbose_name='Mobile Image Alignment (horizontal)', choices=[(b'left', 'Left'), (b'center', 'Center'), (b'right', 'Right')])),
                ('bg_image_inner_container', filer.fields.image.FilerImageField(related_name='content_container_bg_image', blank=True, to='filer.Image', help_text='Dimensions TBD', null=True, verbose_name='Background-Image')),
                ('bg_image_outer_container', filer.fields.image.FilerImageField(related_name='content_bg_image', blank=True, to='filer.Image', help_text='Dimensions TBD', null=True, verbose_name='Background-Image')),
                ('video_file', filer.fields.file.FilerFileField(related_name='content_video_file', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='filer.File', help_text='Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 4 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>Aspect ratio: TBD<br>File size: Dependent of video length. Generally speaking: Less is more.', null=True, verbose_name='Source')),
                ('video_mobile_image', filer.fields.image.FilerImageField(related_name='content_video_moible_image', blank=True, to='filer.Image', help_text='The image being displayed on mobile devices. Dimensions TBD', null=True, verbose_name='Mobile Image')),
                ('video_poster_image', filer.fields.image.FilerImageField(related_name='content_video_poster_image', blank=True, to='filer.Image', help_text='This image is displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.', null=True, verbose_name='Video Start Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
