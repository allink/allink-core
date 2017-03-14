# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0015_auto_20170313_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkbuttonlinkplugin',
            name='link_target_old',
        ),
        migrations.RemoveField(
            model_name='allinkbuttonlinkplugin',
            name='softpage_enabled',
        ),
    ]
