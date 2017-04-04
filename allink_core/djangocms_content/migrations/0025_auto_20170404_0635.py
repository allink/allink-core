# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0024_allinkcontentcolumnplugin_alignment_vertikal_desktop'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allinkcontentcolumnplugin',
            old_name='alignment_vertikal_desktop',
            new_name='alignment_vertical_desktop',
        ),
    ]
