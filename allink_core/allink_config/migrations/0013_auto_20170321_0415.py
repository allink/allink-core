# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0012_auto_20170301_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkconfig',
            name='locations_verbose',
            field=models.CharField(default='Emplacement', max_length=255, verbose_name='Locations verbose name'),
        ),
    ]
