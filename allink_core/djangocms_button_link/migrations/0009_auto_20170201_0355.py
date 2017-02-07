# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0008_auto_20170201_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='softpage_enabled',
            field=models.BooleanField(default=False, help_text='If checked, the content will be displayed in a "softpage". (Is currently only working with content of special links.))', verbose_name='Show in Softpage'),
        ),
    ]
