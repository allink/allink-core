# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0003_allinklegacylink_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinklegacylink',
            name='new',
            field=cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='New Page', to='cms.Page', help_text='If provided, overrides the external link.', null=True),
        ),
    ]
