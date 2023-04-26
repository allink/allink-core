# Generated by Django 3.2.12 on 2022-04-14 13:43

import cms.models.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('allink_legacy_redirect', '0002_auto_20220317_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinklegacylink',
            name='link_page',
            field=cms.models.fields.PageField(help_text='If provided, overrides the external link and New Apphook-Page.', null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.page', verbose_name='New Page'),
        ),
    ]
