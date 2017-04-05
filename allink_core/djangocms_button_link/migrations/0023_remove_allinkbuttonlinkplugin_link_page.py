# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0022_allinkbuttonlinkplugin_link_internal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkbuttonlinkplugin',
            name='link_page',
        ),
    ]
