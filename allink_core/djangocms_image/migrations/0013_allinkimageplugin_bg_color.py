# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0012_auto_20170404_0632'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkimageplugin',
            name='bg_color',
            field=models.CharField(max_length=50, null=True, verbose_name='Set a predefined background color', blank=True),
        ),
    ]
