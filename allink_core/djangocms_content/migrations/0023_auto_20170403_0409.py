# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0022_auto_20170322_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='bg_color',
            field=models.CharField(max_length=50, null=True, verbose_name='Set a predefined background color', blank=True),
        ),
    ]
