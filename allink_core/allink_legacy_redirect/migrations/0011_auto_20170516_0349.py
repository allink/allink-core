# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0010_auto_20170510_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinklegacylink',
            name='link_model',
            field=models.CharField(max_length=300, help_text='Dotted Path to referenced Model', null=True),
        ),
        migrations.AddField(
            model_name='allinklegacylink',
            name='link_url_kwargs',
            field=django.contrib.postgres.fields.ArrayField(null=True, help_text='Keyword arguments used to reverse url.', blank=True, base_field=models.CharField(max_length=50, null=True, blank=True), size=None),
        ),
    ]
