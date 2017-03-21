# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import allink_core.allink_base.models.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0004_auto_20170214_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinklegacylink',
            name='new_page',
            field=allink_core.allink_base.models.model_fields.SitemapField(help_text='If provided, gets overriden by external link.', null=True, verbose_name='New Page'),
        ),
    ]
