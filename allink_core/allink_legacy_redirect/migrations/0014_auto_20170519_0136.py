# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cms.models.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0013_auto_20170517_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinklegacylink',
            name='link_apphook_page',
            field=cms.models.fields.PageField(null=True, verbose_name='New Apphook-Page', related_name='allink_legacy_redirect_allinklegacylink_app_legacy_redirects', help_text='If provided, overrides the external link.', on_delete=django.db.models.deletion.SET_NULL, to='cms.Page'),
        ),
    ]
