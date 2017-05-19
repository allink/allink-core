# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
import cms.models.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('djangocms_button_link', '0026_allinkbuttonlinkcontainerplugin_project_css_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='link_apphook_page',
            field=cms.models.fields.PageField(null=True, verbose_name='New Apphook-Page', related_name='djangocms_button_link_allinkbuttonlinkplugin_app_legacy_redirects', help_text='If provided, overrides the external link.', on_delete=django.db.models.deletion.SET_NULL, to='cms.Page'),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='link_model',
            field=models.CharField(null=True, max_length=300, help_text='Dotted Path to referenced Model'),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='link_object_id',
            field=models.IntegerField(null=True, help_text='To which object directs the url.'),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='link_page',
            field=cms.models.fields.PageField(null=True, verbose_name='New Page', help_text='If provided, overrides the external link and New Apphook-Page.', on_delete=django.db.models.deletion.SET_NULL, to='cms.Page'),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='link_url_kwargs',
            field=django.contrib.postgres.fields.ArrayField(null=True, base_field=models.CharField(null=True, blank=True, max_length=50), blank=True, size=None, help_text='Keyword arguments used to reverse url.'),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='link_url_name',
            field=models.CharField(null=True, max_length=64, help_text='Name of the App-URL to use.'),
        ),
    ]
