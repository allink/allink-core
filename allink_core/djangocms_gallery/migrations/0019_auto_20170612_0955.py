# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0018_auto_20170608_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgalleryimageplugin',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(verbose_name='Text', blank=True, null=True),
        ),
    ]
