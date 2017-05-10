# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_vid', '0009_auto_20170510_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkvidembedplugin',
            name='video_id',
            field=models.CharField(max_length=255, help_text='Only provide the ID. The correct URL will automatically be generated.<br><br>YouTube: https://www.youtube.com/watch?v=<strong>12345678</strong> (the ID is <strong>12345678</strong>)<br>Vimeo: https://vimeo.com/<strong>12345678</strong> (the ID is <strong>12345678</strong>)', verbose_name='Video ID'),
        ),
    ]
