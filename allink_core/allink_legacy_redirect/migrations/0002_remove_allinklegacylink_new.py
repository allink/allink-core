# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinklegacylink',
            name='new',
        ),
    ]
