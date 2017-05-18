# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def delte_default_values(apps, schema_editor):
    AllinkConfig = apps.get_model('allink_config', 'AllinkConfig')

    conf = AllinkConfig.objects.get(id=1)

    conf.theme_color = None
    conf.mask_icon_color = None
    conf.msapplication_tilecolor = None

    conf.save()


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0023_auto_20170518_0125'),
    ]

    operations = [
        migrations.RunPython(delte_default_values),
    ]
