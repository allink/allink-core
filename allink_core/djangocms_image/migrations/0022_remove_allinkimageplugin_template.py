# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0021_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkimageplugin',
            name='template',
        ),
    ]
