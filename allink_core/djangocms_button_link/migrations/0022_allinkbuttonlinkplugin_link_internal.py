# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import allink_core.allink_base.models.model_fields

from cms.models import Page


def transfer_links(apps, schema_editor):
    AllinkButtonLinkPlugin = apps.get_model('djangocms_button_link', 'AllinkButtonLinkPlugin')

    for link in AllinkButtonLinkPlugin.objects.filter(link_page__isnull=False):
        link.link_internal = Page.objects.get(id=link.link_page.id).get_absolute_url(language=link.language)
        link.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0021_auto_20170322_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='link_internal',
            field=allink_core.allink_base.models.model_fields.SitemapField(help_text='If provided, overrides the external link.', null=True, verbose_name='Internal link', blank=True),
        ),
        migrations.RunPython(transfer_links)
    ]
