# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0021_auto_20170411_0453'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkconfig',
            name='google_site_verification',
            field=models.CharField(verbose_name='Google Site Verification Code', blank=True, null=True, max_length=64),
        ),
    ]
