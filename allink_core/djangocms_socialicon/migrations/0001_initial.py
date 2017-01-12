# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkSocialIconContainerPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_socialicon_allinksocialiconcontainerplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='AllinkSocialIconPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_socialicon_allinksocialiconplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
                ('link', cms.models.fields.PageField(to='cms.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
