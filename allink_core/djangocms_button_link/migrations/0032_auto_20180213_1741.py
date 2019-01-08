# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0031_auto_20170823_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='allow_fullscreen_enabled',
            field=models.BooleanField(verbose_name='Allow fullscreen', default=True),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='auto_start_enabled',
            field=models.BooleanField(help_text='<strong>Important:</strong> Autoplaying videos with audio is not recommended. Use wisely. ', verbose_name='Autostart', default=False),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='ratio',
            field=models.CharField(null=True, verbose_name='Ratio', max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='video_id',
            field=models.CharField(help_text='Only provide the ID. The correct URL will automatically be generated.<br><br>YouTube: https://www.youtube.com/watch?v=<strong>12345678</strong> (the ID is <strong>12345678</strong>)<br>Vimeo: https://vimeo.com/<strong>12345678</strong> (the ID is <strong>12345678</strong>)', null=True, verbose_name='Video ID', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='video_service',
            field=models.CharField(null=True, verbose_name='Video Service', max_length=50, blank=True, choices=[('youtube', 'Youtube'), ('vimeo', 'Vimeo')]),
        ),
    ]
