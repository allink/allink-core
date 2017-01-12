# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0006_auto_20160623_1627'),
        ('allink_config', '0002_auto_20170110_0419'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkconfig',
            name='default_og_image',
            field=filer.fields.image.FilerImageField(blank=True, to='filer.Image', help_text='Default image when shared on Facebook.', null=True, verbose_name='og:Image'),
        ),
    ]
