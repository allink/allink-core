# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0028_auto_20170607_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkmetatagextension',
            name='override_h1',
            field=models.CharField(blank=True, help_text='Page Title or App title is default. This option allows you to override the h1 tag.', null=True, max_length=255, verbose_name='Override H1'),
        ),
    ]
