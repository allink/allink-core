# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0008_auto_20170322_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinklegacylink',
            name='match_subpages',
            field=models.BooleanField(default=False, help_text='If True, matches all subpages and redirects them to this link.', verbose_name='Match subpages'),
        ),
    ]
