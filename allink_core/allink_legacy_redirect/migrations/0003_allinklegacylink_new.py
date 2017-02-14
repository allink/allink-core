# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('allink_legacy_redirect', '0002_remove_allinklegacylink_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinklegacylink',
            name='new',
            field=cms.models.fields.PageField(to='cms.Page', null=True),
        ),
    ]
