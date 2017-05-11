# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0023_remove_allinkimageplugin_external_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkimageplugin',
            name='use_no_cropping',
        ),
        migrations.RemoveField(
            model_name='allinkimageplugin',
            name='width',
        ),
    ]
