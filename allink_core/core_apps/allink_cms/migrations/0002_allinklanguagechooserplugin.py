# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-21 10:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('allink_cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkLanguageChooserPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_cms_allinklanguagechooserplugin', serialize=False, to='cms.CMSPlugin')),
            ],
            bases=('cms.cmsplugin',),
        ),
    ]
