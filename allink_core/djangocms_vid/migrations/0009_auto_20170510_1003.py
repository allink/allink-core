# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_vid', '0008_auto_20170510_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkvidembedplugin',
            name='auto_start_enabled',
            field=models.BooleanField(verbose_name='Autostart', help_text='<strong>Important:</strong> Autoplaying videos with audio is not recommended. Use wisely. ', default=False),
        ),
        migrations.AlterField(
            model_name='allinkvidfileplugin',
            name='video_file',
            field=filer.fields.file.FilerFileField(verbose_name='Video File', on_delete=django.db.models.deletion.SET_NULL, help_text='Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>File size: Dependent of video length. Generally speaking: Less is more.', related_name='djangocms_vid_allinkvidfileplugin_video_file', to='filer.File', null=True),
        ),
        migrations.AlterField(
            model_name='allinkvidfileplugin',
            name='video_poster_image',
            field=filer.fields.image.FilerImageField(verbose_name='Video Start Image', help_text='Image that is being displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.<br><br><strong>Imoprtant:</strong> Make sure the aspect ratio of the image is <strong>exactly the same</strong> as the video, otherwise the video height will shrink or grow when the playback starts.', related_name='djangocms_vid_allinkvidfileplugin_video_poster_image', to='filer.Image', null=True),
        ),
    ]
