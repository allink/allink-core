# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def migrate_bg_color(apps, schema_editor):
    Plugin = apps.get_model('djangocms_content', 'AllinkContentPlugin')

    for plugin in Plugin.objects.all():
        if plugin.bg_color == '1':
            plugin.bg_color = 'project-color-1'
        elif plugin.bg_color == '2':
            plugin.bg_color = 'project-color-2'
        elif plugin.bg_color == '3':
            plugin.bg_color = 'project-color-3'
        plugin.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0013_auto_20170315_0343'),
    ]

    operations = [
        migrations.RunPython(migrate_bg_color)
    ]
