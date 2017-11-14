# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0030_auto_20170619_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_url',
            field=models.URLField(help_text='Provide a valid URL to an external website.', max_length=500, default='', blank=True, verbose_name='External link'),
        ),
    ]
