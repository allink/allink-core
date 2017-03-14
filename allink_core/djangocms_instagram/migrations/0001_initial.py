# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkInstagramPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_instagram_allinkinstagramplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(help_text='The section title', max_length=255, null=True, verbose_name='Title', blank=True)),
                ('template', models.CharField(default=(b'grid_static', b'Grid (Static)'), help_text='Choose a template.', max_length=50, verbose_name='Template', choices=[(b'grid_static', b'Grid (Static)')])),
                ('ordering', models.CharField(default=(b'default', b'---------'), help_text='Choose a order.', max_length=50, verbose_name='Sort order', choices=[(b'default', b'---------'), (b'latest', b'latest first'), (b'random', b'random')])),
                ('items_per_row', models.IntegerField(default=3, help_text='Only applied if a "Grid" template has been selected.', verbose_name='Grid items per row', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])),
                ('paginated_by', models.IntegerField(default=9, help_text='Set to 0 if all entries should be displayed on first page.', verbose_name='Max. entries per page')),
                ('account', models.CharField(help_text='Instagram account name', max_length=255, verbose_name='Account')),
                ('follow_text', models.CharField(help_text='Follow us text i.e.: Tag your images with #awesomehashtag', max_length=255, null=True, verbose_name='Follow Text', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
