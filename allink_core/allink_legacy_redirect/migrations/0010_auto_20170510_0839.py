# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('allink_legacy_redirect', '0009_auto_20170323_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinklegacylink',
            name='new',
        ),
        migrations.AddField(
            model_name='allinklegacylink',
            name='link_apphook_page',
            field=cms.models.fields.PageField(help_text='If provided, overrides the external link.', to='cms.Page', verbose_name='New Apphook-Page', on_delete=django.db.models.deletion.SET_NULL, related_name='app_legacy_redirects', null=True),
        ),
        migrations.AddField(
            model_name='allinklegacylink',
            name='link_object_id',
            field=models.IntegerField(help_text='To which object directs the url.', null=True),
        ),
        migrations.AddField(
            model_name='allinklegacylink',
            name='link_page',
            field=cms.models.fields.PageField(help_text='If provided, overrides the external link and New Apphook-Page.', to='cms.Page', verbose_name='New Page', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='allinklegacylink',
            name='link_url_name',
            field=models.CharField(help_text='Name of the App-URL to use.', max_length=64, null=True),
        ),
    ]
