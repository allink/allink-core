# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-21 09:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkPdfPageBreakPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_pdf_allinkpdfpagebreakplugin', serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]