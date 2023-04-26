# Generated by Django 3.2.12 on 2022-03-17 11:33

import cms.models.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('allink_legacy_redirect', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinklegacylink',
            name='link_apphook_page',
            field=cms.models.fields.PageField(help_text='If provided, overrides the external link.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='allink_legacy_redirect_allinklegacylink_app_legacy_redirects', to='cms.page', verbose_name='New Apphook-Page'),
        ),
        migrations.AlterField(
            model_name='allinklegacylink',
            name='link_page',
            field=cms.models.fields.PageField(help_text='If provided, overrides the external link and New Apphook-Page.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.page', verbose_name='New Page'),
        ),
    ]
