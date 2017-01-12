# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_socialicon', '0002_auto_20170109_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinksocialiconplugin',
            name='icon',
            field=models.CharField(max_length=50, verbose_name='Icon', choices=[(b'facebook', 'Facebook'), (b'instagram', 'Instagram'), (b'pinterest', 'Pinterest'), (b'twitter', 'Twitter'), (b'snapchat', 'Snapchat'), (b'linkedin', 'Linkedin'), (b'spotify', 'Spotify'), (b'xing', 'Xing'), (b'youtube', 'Youtube'), (b'vimeo', 'Vimeo'), (b'googleplus', 'Google Plus')]),
        ),
        migrations.AlterField(
            model_name='allinksocialiconplugin',
            name='title',
            field=models.CharField(help_text='SEO text (not visible) e.g. Follow allink on Instagram', max_length=255, null=True, verbose_name='Title', blank=True),
        ),
    ]
