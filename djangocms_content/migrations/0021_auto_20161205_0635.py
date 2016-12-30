# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0020_auto_20161204_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='parallax_enabled',
            field=models.BooleanField(default=False, help_text='If checked, the parallax effect is enabled.', verbose_name='Activate Parallax effect'),
        ),
    ]
