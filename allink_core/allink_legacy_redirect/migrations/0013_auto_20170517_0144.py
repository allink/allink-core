# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0012_auto_20170516_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinklegacylink',
            name='overwrite',
            field=models.CharField(null=True, help_text="Overwrites 'New Page', use for special urls that are not listed there", max_length=255, blank=True, verbose_name='Overwrite Link'),
        ),
    ]
