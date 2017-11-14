# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.folder


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        ('djangocms_gallery', '0019_auto_20170612_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkgalleryplugin',
            name='folder',
            field=filer.fields.folder.FilerFolderField(to='filer.Folder', blank=True, null=True, help_text="All Images (.png, .gif, .jpg, .jpeg) will be used in gallery. If a folder is specified, the child plugin won't be rendered."),
        ),
    ]
