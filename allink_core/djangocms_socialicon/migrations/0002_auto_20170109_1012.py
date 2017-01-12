# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_socialicon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinksocialiconplugin',
            name='icon',
            field=models.CharField(default='facebook', max_length=50, verbose_name='Icon', choices=[(b'facebook', 'Facebook'), (b'instagram', 'Instagram'), (b'piterest', 'Piterest'), (b'twitter', 'Twitter'), (b'snapchat', 'Snapchat'), (b'linkedin', 'Linkedin'), (b'spotify', 'Spotify'), (b'xing', 'Xing'), (b'youtube', 'Youtube'), (b'vimeo', 'Vimeo'), (b'googleplus', 'Google Plus')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='allinksocialiconplugin',
            name='link',
            field=models.URLField(verbose_name='Link'),
        ),
    ]
