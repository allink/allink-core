# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import allink_core.djangocms_button_link.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0034_auto_20180214_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='template',
            field=models.CharField(help_text='Choose a link type in order to display its options below.', choices=[('default_link', 'Internal/External Link'), ('phone_link', 'Phone Link'), ('email_link', 'Email Link'), ('form_link', 'Form Link'), ('video_embedded_link', 'Video (Embedded)'), ('video_file_link', 'Video (File)')], max_length=50, verbose_name='Link type', default='default_link'),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='type',
            field=allink_core.djangocms_button_link.model_fields.LinkOrButton(max_length=255, verbose_name='Type', default='lnk'),
        ),
    ]
