# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0027_auto_20161207_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='container_enabled',
            field=models.BooleanField(default=True, help_text='If checked, an inner container with a maximum width is added', verbose_name='Activate "container"'),
        ),
    ]
