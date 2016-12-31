# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0006_auto_20160623_1627'),
        ('djangocms_content', '0022_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='video_file',
            field=filer.fields.file.FilerFileField(related_name='content_video_file', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Source', to='filer.File', help_text='Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 4 (video load quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>Aspect ratio: TBD<br>File size: Dependet of length of video. Generally speaking: Less is more.', null=True),
        ),
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='video_mobile_image',
            field=filer.fields.image.FilerImageField(related_name='content_video_moible_image', blank=True, to='filer.Image', help_text='The image being displayed on mobile devices. Dimensions TBD', null=True, verbose_name='Mobile Image'),
        ),
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='video_mobile_image_alignment',
            field=models.CharField(default=b'center', help_text='TBD Definieren Sie wo sich das wichtigste Element des Bildes befindet. Standardm\xe4ssig nutzt das Bild den verf\xfcgbaren Platz. Dabei kannn das Bild etwas angeschnitten werden. Je nach Bild befindet sich das wichtigste Element links, in der Mitte oder rechts.', max_length=6, verbose_name='Ausrichtung (Mobile Bild)', choices=[(b'left', 'Left'), (b'center', 'Center'), (b'right', 'Right')]),
        ),
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='video_poster_image',
            field=filer.fields.image.FilerImageField(related_name='content_video_poster_image', blank=True, to='filer.Image', help_text='This image is displayed while the video is loading. Ideally the very first frame of the video is used, in to make the transition as smooth as possible.', null=True, verbose_name='Video Start Image'),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='bg_image_inner_container',
            field=filer.fields.image.FilerImageField(related_name='content_container_bg_image', blank=True, to='filer.Image', help_text='Dimensions TBD', null=True, verbose_name='Background-Image'),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='bg_image_outer_container',
            field=filer.fields.image.FilerImageField(related_name='content_bg_image', blank=True, to='filer.Image', help_text='Dimensions TBD', null=True, verbose_name='Background-Image'),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='template',
            field=models.CharField(default=(b'col-1', b'1 Column'), help_text='Choose a template. The template can NOT be changed after the content has been saved.', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-1-2', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')]),
        ),
    ]
