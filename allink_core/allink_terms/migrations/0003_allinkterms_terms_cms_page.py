# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('allink_terms', '0002_auto_20170220_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkterms',
            name='terms_cms_page',
            field=cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cms.Page', help_text='CMS Page which shows Terms and Conditions', null=True, verbose_name='Terms cms Page'),
        ),
    ]
