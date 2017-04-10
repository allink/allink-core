# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0011_auto_20170322_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='ratio',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Ratio', choices=[(b'3-2', b'3:2'), (b'2-1', b'2:1'), (b'4-3', b'4:3'), (b'1-1', b'1:1'), (b'16-9', b'16:9'), (b'x-y', b'Original')]),
        ),
    ]
