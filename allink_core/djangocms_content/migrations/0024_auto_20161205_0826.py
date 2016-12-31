# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0023_auto_20161205_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='video_file',
            field=filer.fields.file.FilerFileField(related_name='content_video_file', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='filer.File', help_text='Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 4 (video load quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>Aspect ratio: TBD<br>File size: Dependet of length of video. Generally speaking: Less is more.', null=True, verbose_name='Source'),
        ),
    ]
