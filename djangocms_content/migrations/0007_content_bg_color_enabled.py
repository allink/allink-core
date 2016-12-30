# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0006_auto_20161114_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='bg_color_enabled',
            field=models.BooleanField(default=True, verbose_name='Set a predefined background color'),
        ),
    ]
