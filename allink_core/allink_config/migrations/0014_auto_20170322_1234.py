# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0013_auto_20170321_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkconfig',
            name='locations_verbose',
            field=models.CharField(default='Location', max_length=255, verbose_name='Locations verbose name'),
        ),
    ]
