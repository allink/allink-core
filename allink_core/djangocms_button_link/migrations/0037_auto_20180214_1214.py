# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_button_template(apps, schema_editor):
    AllinkButtonLinkPlugin = apps.get_model('djangocms_button_link', 'AllinkButtonLinkPlugin')

    DEFAULT_LINK = 'default_link'
    FILE_LINK = 'file_link'
    IMAGE_LINK = 'image_link'
    PHONE_LINK = 'phone_link'
    EMAIL_LINK = 'email_link'
    FORM_LINK = 'form_link'
    # VIDEO_EMBEDDED_LINK = 'video_embedded_link'

    # NEW_WINDOW = 1
    # SOFTPAGE_LARGE = 2
    # SOFTPAGE_SMALL = 3
    FORM_MODAL = 4
    IMAGE_MODAL = 5

    for plugin in AllinkButtonLinkPlugin.objects.all():
        if plugin.link_file and not plugin.link_target == IMAGE_MODAL:
            plugin.template = FILE_LINK
        elif plugin.link_target == IMAGE_MODAL:
            plugin.template = IMAGE_LINK
        elif plugin.link_phone:
            plugin.template = PHONE_LINK
        elif plugin.link_mailto:
            plugin.template = EMAIL_LINK
        elif plugin.link_target == FORM_MODAL:
            plugin.template = FORM_LINK
        else:
            plugin.template = DEFAULT_LINK
        plugin.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0036_auto_20180214_1214'),
    ]

    operations = [
        migrations.RunPython(migrate_button_template),
    ]
