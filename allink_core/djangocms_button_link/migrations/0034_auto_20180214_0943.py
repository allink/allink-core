# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import allink_core.djangocms_button_link.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0033_allinkbuttonlinkplugin_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='template',
            field=models.CharField(choices=[('default_link', 'Internal/External'), ('video_embedded_link', 'Video (Embedded)')], verbose_name='Link type', help_text='Choose a link type in order to display its options below.', default='default_link', max_length=50),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='type',
            field=allink_core.djangocms_button_link.model_fields.LinkOrButton(verbose_name='Display type', default='lnk', max_length=255),
        ),
    ]
