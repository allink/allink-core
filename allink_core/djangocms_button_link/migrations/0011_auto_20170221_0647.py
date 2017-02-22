# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0010_auto_20170202_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_file',
            field=filer.fields.file.FilerFileField(verbose_name='file', blank=True, to='filer.File', null=True),
        ),
    ]
