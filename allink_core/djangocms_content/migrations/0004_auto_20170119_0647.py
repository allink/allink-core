# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0003_auto_20170117_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='bg_image_outer_container',
            field=filer.fields.image.FilerImageField(related_name='djangocms_content_allinkcontentplugin_bg_image', blank=True, to='filer.Image', help_text='Dimensions TBD', null=True, verbose_name='Background-Image'),
        ),
    ]
