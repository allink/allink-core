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
            name='AllinkInstagramPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_instagram_allinkinstagramplugin', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, help_text='The section title', max_length=255, null=True, verbose_name='Title')),
                ('template', models.CharField(help_text='Choose a template.', max_length=50, verbose_name='Template')),
                ('ordering', models.CharField(choices=[('default', '---------'), ('latest', 'latest first'), ('random', 'random')], default=('default', '---------'), help_text='Choose a order.', max_length=50, verbose_name='Sort order')),
                ('items_per_row', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], default=3, help_text='Only applied if a "Grid" template has been selected.', verbose_name='Grid items per row')),
                ('paginated_by', models.IntegerField(default=9, help_text='Set to 0 if all entries should be displayed on first page.', verbose_name='Max. entries per page')),
                ('account', models.CharField(help_text='Instagram account name', max_length=255, verbose_name='Account')),
                ('follow_text', models.CharField(blank=True, help_text='Follow us text i.e.: Tag your images with #awesomehashtag', max_length=255, null=True, verbose_name='Follow Text')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
