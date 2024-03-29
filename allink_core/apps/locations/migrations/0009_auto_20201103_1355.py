# Generated by Django 2.2.13 on 2020-11-03 13:55

import cms.models.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('locations', '0008_auto_20201102_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationsappcontentplugin',
            name='load_more_link',
        ),
        migrations.AddField(
            model_name='locationsappcontentplugin',
            name='load_more_internallink',
            field=cms.models.fields.PageField(blank=True, help_text='Link for Button Below Items if custom URL is chosen', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='load_more_internallink_locations', to='cms.Page', verbose_name='Custom Load More Link'),
        ),
    ]
