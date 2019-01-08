# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0035_auto_20180214_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_special',
            field=models.CharField(max_length=255, blank=True, verbose_name='Form', null=True),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='template',
            field=models.CharField(max_length=50, help_text='Choose a link type in order to display its options below.', default='default_link', choices=[('default_link', 'Internal/External'), ('file_link', 'File (Download)'), ('image_link', 'Image'), ('phone_link', 'Phone'), ('email_link', 'Email'), ('form_link', 'Form'), ('video_embedded_link', 'Video (Embedded)')], verbose_name='Link type'),
        ),
    ]
