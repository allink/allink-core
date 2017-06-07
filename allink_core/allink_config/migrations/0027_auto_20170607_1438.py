# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0026_auto_20170531_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkmetatagextension',
            name='og_description',
        ),
        migrations.RemoveField(
            model_name='allinkmetatagextension',
            name='og_title',
        ),
    ]
