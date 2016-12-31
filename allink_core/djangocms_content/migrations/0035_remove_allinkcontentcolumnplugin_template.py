# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0034_auto_20161223_0710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkcontentcolumnplugin',
            name='template',
        ),
    ]
