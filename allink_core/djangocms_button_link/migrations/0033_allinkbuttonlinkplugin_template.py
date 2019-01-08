# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0032_auto_20180213_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='template',
            field=models.CharField(max_length=50, default='default_link', choices=[('default_link', 'Internal/External'), ('video_embedded_link', 'Video (Embedded)')], help_text='Choose a template.', verbose_name='Template'),
        ),
    ]
