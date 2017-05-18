# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0022_allinkconfig_google_site_verification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkconfig',
            name='mask_icon_color',
            field=models.CharField(null=True, blank=True, max_length=7, verbose_name='Mask icon color', help_text='Mask icon color for safari-pinned-tab.svg'),
        ),
        migrations.AlterField(
            model_name='allinkconfig',
            name='msapplication_tilecolor',
            field=models.CharField(null=True, blank=True, max_length=7, verbose_name='msapplication TileColor', help_text='MS application TitleColor Field'),
        ),
        migrations.AlterField(
            model_name='allinkconfig',
            name='theme_color',
            field=models.CharField(null=True, blank=True, max_length=7, verbose_name='Theme Color', help_text='Theme color for Android Chrome'),
        ),
    ]
