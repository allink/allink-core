# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import cms.models.fields
import allink_core.allink_base.models.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0005_allinklegacylink_new_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinklegacylink',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Actif'),
        ),
        migrations.AlterField(
            model_name='allinklegacylink',
            name='new',
            field=cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Nouvelle page', to='cms.Page', help_text='If provided, overrides the external link.', null=True),
        ),
        migrations.AlterField(
            model_name='allinklegacylink',
            name='new_page',
            field=allink_core.allink_base.models.model_fields.SitemapField(help_text='If provided, gets overriden by external link.', null=True, verbose_name='Nouvelle page'),
        ),
    ]
