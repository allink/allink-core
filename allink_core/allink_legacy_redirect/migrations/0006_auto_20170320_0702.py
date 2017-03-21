# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def transfer_url_values(apps, schema_editor):
    AllinkLegacyLink = apps.get_model('allink_legacy_redirect', 'AllinkLegacyLink')
    from cms.models.pagemodel import Page
    for link in AllinkLegacyLink.objects.all():
        if not link.overwrite:
            link.new_page = Page.objects.get(id=link.new.id).get_absolute_url()
            link.save()


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0005_allinklegacylink_new_page'),
        ('cms', '0016_auto_20160608_1535')
    ]

    operations = [
        migrations.RunPython(transfer_url_values),
    ]
