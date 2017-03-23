# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0007_auto_20170321_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgalleryimageplugin',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(null=True, verbose_name='Text', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkgalleryimageplugin',
            name='title',
            field=models.CharField(max_length=255, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkgalleryplugin',
            name='template',
            field=models.CharField(default=(b'slider', b'Slider'), help_text='Choose a template.', max_length=50, verbose_name='Template', choices=[(b'slider', b'Slider')]),
        ),
        migrations.AlterField(
            model_name='allinkgalleryplugin',
            name='title',
            field=models.CharField(help_text='The section title', max_length=255, null=True, verbose_name='Title', blank=True),
        ),
    ]
