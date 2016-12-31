# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0007_content_bg_color_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='bg_color_enabled',
            field=models.BooleanField(default=False, verbose_name='Set a predefined background color'),
        ),
    ]
