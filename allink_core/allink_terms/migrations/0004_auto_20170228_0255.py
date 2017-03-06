# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('allink_terms', '0003_allinkterms_terms_cms_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkterms',
            name='terms_cms_page',
            field=cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Terms cms Page', to='cms.Page', help_text='CMS Page which shows Terms and Conditions', null=True),
        ),
    ]
