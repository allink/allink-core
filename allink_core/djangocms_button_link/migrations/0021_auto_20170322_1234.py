# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import djangocms_attributes_field.fields
import allink_core.djangocms_button_link.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0020_auto_20170321_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='btn_size',
            field=allink_core.djangocms_button_link.model_fields.Size(default='md', max_length=255, verbose_name='Size', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_attributes',
            field=djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_file',
            field=filer.fields.file.FilerFileField(verbose_name='file', blank=True, to='filer.File', null=True),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_mailto',
            field=models.EmailField(max_length=255, null=True, verbose_name='Email address', blank=True),
        ),
    ]
