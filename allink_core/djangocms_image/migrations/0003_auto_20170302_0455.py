# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def copy_old_plugin(apps, schema_editor):
    OldPlugin = apps.get_model("djangocms_picture", "Picture")
    NewPlugin = apps.get_model("djangocms_image", "AllinkImagePlugin")


    for old in OldPlugin.objects.all():
        new = NewPlugin()

        new.position = old.position
        new.language = old.language
        new.plugin_type = 'CMSAllinkImagePlugin'
        new.creation_date = old.creation_date
        new.changed_date = old.changed_date
        new.parent_id = old.parent_id
        new.placeholder_id = old.placeholder_id
        new.depth = old.depth
        new.numchild = old.numchild
        new.path = old.path

        new.cmsplugin_ptr_id = old.cmsplugin_ptr_id
        new.link_url = old.link_url
        new.link_page_id = old.link_page_id
        new.width = old.width
        new.picture_id = old.picture_id
        new.attributes = old.attributes
        new.caption_text = old.caption_text
        new.link_attributes = old.link_attributes
        new.softpage_enabled = True if 'data-toggle-image-modal' in old.link_attributes else False
        new.link_target = True if old.link_target == '_blank' else False
        new.use_no_cropping = old.use_no_cropping
        new.external_picture = old.external_picture
        new.template = old.template

        new.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0002_allinkimageplugin_softpage_enabled'),
        ('djangocms_picture', '0007_fix_alignment'),
    ]

    operations = [
        migrations.RunPython(copy_old_plugin),
    ]
