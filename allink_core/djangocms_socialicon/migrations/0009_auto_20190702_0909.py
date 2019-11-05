# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_socialicon', '0008_auto_20170407_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinksocialiconplugin',
            name='icon',
            field=models.CharField(verbose_name='Icon', choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('pinterest', 'Pinterest'), ('twitter', 'Twitter'), ('snapchat', 'Snapchat'), ('linkedin', 'Linkedin'), ('spotify', 'Spotify'), ('xing', 'Xing'), ('youtube', 'Youtube'), ('vimeo', 'Vimeo'), ('tripadvisor', 'TripAdvisor'), ('kununu', 'kununu')], max_length=50),
        ),
    ]
