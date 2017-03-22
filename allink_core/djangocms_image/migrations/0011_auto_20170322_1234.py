# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import djangocms_attributes_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0010_auto_20170321_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='attributes',
            field=djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='caption_text',
            field=models.TextField(help_text='Provide a description, attribution, copyright or other information.', verbose_name='Caption text', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='external_picture',
            field=models.URLField(help_text='If provided, overrides the embedded image. Certain options such as cropping are not applicable to external images.', max_length=255, verbose_name='External image', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_attributes',
            field=djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_file',
            field=filer.fields.file.FilerFileField(verbose_name='file', blank=True, to='filer.File', null=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_mailto',
            field=models.EmailField(max_length=255, null=True, verbose_name='Email address', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='template',
            field=models.CharField(default=(b'default', b'Default'), help_text='Choose a template.', max_length=50, verbose_name='Template', choices=[(b'default', b'Default')]),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='use_no_cropping',
            field=models.BooleanField(default=False, help_text='Outputs the raw image without cropping.', verbose_name='Use original image'),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='width',
            field=models.PositiveIntegerField(help_text='The image width as number in pixels. Example: "720" and not "720px".', null=True, verbose_name='Width', blank=True),
        ),
    ]
