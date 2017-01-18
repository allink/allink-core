# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_socialicon', '0003_auto_20170111_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinksocialiconplugin',
            name='icon',
            field=models.CharField(max_length=50, verbose_name='Icon', choices=[(b'facebook', 'Facebook'), (b'instagram', 'Instagram'), (b'pinterest', 'Pinterest'), (b'twitter', 'Twitter'), (b'snapchat', 'Snapchat'), (b'linkedin', 'Linkedin'), (b'spotify', 'Spotify'), (b'xing', 'Xing'), (b'youtube', 'Youtube'), (b'vimeo', 'Vimeo'), (b'googleplus', 'Google Plus'), (b'tripadvisor', 'TripAdvisor')]),
        ),
    ]
