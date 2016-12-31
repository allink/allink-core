# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0013_auto_20161201_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkcontent',
            name='bg_color_enabled',
        ),
        migrations.RemoveField(
            model_name='allinkcontent',
            name='container_enabled',
        ),
    ]
