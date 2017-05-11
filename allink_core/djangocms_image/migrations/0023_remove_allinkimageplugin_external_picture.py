# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0022_remove_allinkimageplugin_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkimageplugin',
            name='external_picture',
        ),
    ]
