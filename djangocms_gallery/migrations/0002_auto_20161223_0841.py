# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkgalleryimageplugin',
            name='description',
        ),
        migrations.AddField(
            model_name='allinkgalleryimageplugin',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(null=True, verbose_name='Text', blank=True),
        ),
    ]
