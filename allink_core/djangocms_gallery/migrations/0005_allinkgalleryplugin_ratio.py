# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0004_auto_20170110_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkgalleryplugin',
            name='ratio',
            field=models.CharField(choices=[(b'2-1', b'2:1'), (b'4-3', b'4:3'), (b'1-1', b'1:1'), (b'16-9', b'16:9'), (b'x-y', b'Original')], max_length=50, blank=True, help_text='This option overrides the default settings for the content plugin section.', null=True, verbose_name='Ratio'),
        ),
    ]
