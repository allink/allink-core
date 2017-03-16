# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0012_auto_20170314_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='bg_color',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Set a predefined background color', choices=[(b'project-color-1', b'Project Color 1'), (b'project-color-2', b'Project Color 2'), (b'project-color-3', b'Project Color 3')]),
        ),
    ]
