# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkInfoBoxPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, related_name='allink_info_box_allinkinfoboxplugin', to='cms.CMSPlugin', serialize=False)),
                ('counter', models.IntegerField(verbose_name='Display duration', help_text='After how many times/clicks should the box not be visible anymore', choices=[(0, 'Always visible'), (1, '1x'), (2, '2x'), (3, '3x'), (4, '4x'), (5, '5x')], default=0)),
                ('transparent_background', models.BooleanField(verbose_name='Transparent background', default=False)),
                ('template', models.CharField(verbose_name='Template', max_length=50, help_text='Choose a template.')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
