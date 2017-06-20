# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0032_auto_20170619_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkmetatagextension',
            name='disable_base_title',
        ),
    ]
