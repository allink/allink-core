# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_vid', '0006_auto_20170503_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkvidfileplugin',
            name='poster_only_on_mobile',
            field=models.BooleanField(default=True, help_text='Disable video on mobile devices and only show the start image without video control.', verbose_name='Image Only (Mobile)'),
        ),
    ]
