# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_socialicon', '0007_auto_20170322_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinksocialiconplugin',
            name='icon',
            field=models.CharField(max_length=50, choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('pinterest', 'Pinterest'), ('twitter', 'Twitter'), ('snapchat', 'Snapchat'), ('linkedin', 'Linkedin'), ('spotify', 'Spotify'), ('xing', 'Xing'), ('youtube', 'Youtube'), ('vimeo', 'Vimeo'), ('googleplus', 'Google Plus'), ('tripadvisor', 'TripAdvisor'), ('kununu', 'kununu')], verbose_name='Icon'),
        ),
    ]
