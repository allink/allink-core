# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def link_target(apps, schema_editor):

    Plugin = apps.get_model("djangocms_button_link", "AllinkButtonLinkPlugin")
    for plugin in Plugin.objects.all():
        if plugin.link_target_old:
            plugin.link_target = 1
        elif plugin.softpage_enabled:
            plugin.link_target = 2
        plugin.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0014_allinkbuttonlinkplugin_link_target'),
    ]

    operations = [
        migrations.RunPython(link_target),
    ]
