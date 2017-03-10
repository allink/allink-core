# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_order_mobile(apps, schema_editor):
    AllinkContentColumnPlugin = apps.get_model("djangocms_content", "AllinkContentColumnPlugin")

    for plugin in AllinkContentColumnPlugin.objects.all():
        plugin.order_mobile = plugin.position
        plugin.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0010_allinkcontentcolumnplugin_order_mobile'),
    ]

    operations = [
        migrations.RunPython(migrate_order_mobile),
    ]
