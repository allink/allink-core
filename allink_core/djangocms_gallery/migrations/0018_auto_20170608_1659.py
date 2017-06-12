# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangocms_text_ckeditor.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0017_allinkgalleryplugin_project_css_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgalleryimageplugin',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(null=True, validators=[django.core.validators.MaxLengthValidator(2000)], blank=True, verbose_name='Text'),
        ),
    ]
