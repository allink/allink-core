# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allinkbuttonlinkplugin',
            old_name='title',
            new_name='label',
        ),
    ]
