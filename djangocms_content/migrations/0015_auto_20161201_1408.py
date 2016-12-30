# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0014_auto_20161201_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcontent',
            name='bg_color_enabled',
            field=models.BooleanField(default=False, verbose_name='Set a predefined background color'),
        ),
        migrations.AddField(
            model_name='allinkcontent',
            name='container_enabled',
            field=models.BooleanField(default=True, help_text='If checked, an inner container with a maximum width is added', verbose_name='Display columns within container'),
        ),
    ]
