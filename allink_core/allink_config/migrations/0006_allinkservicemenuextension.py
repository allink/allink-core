# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('allink_config', '0005_auto_20170110_0757'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkServiceMenuExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('in_service_navigation', models.BooleanField(default=False, verbose_name='in navigation')),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Page')),
                ('public_extension', models.OneToOneField(related_name='draft_extension', null=True, editable=False, to='allink_config.AllinkServiceMenuExtension')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
