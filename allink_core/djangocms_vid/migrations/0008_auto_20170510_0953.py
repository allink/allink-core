# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_vid', '0007_auto_20170503_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkvidembedplugin',
            name='auto_start_enabled',
            field=models.BooleanField(default=False, verbose_name='Autostart'),
        ),
    ]
