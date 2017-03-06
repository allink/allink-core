# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('allink_terms', '0004_auto_20170228_0255'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkTermsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='allink_terms_allinktermsplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
