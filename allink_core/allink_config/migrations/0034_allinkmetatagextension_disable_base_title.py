# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0033_remove_allinkmetatagextension_disable_base_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkmetatagextension',
            name='disable_base_title',
            field=models.BooleanField(default=False, help_text='If disabled, only the page title will be shown. Everything behind and including the "|" will be removed.', verbose_name='Disable base title'),
        ),
    ]
