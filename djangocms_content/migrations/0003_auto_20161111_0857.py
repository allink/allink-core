# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('djangocms_content', '0002_auto_20161111_0718'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentColumn',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_content_contentcolumn', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterField(
            model_name='content',
            name='template',
            field=models.CharField(default=b'1_col', max_length=50, verbose_name='Template', choices=[(b'1_col', b'1 \xe2\x80\x93 col')]),
        ),
    ]
