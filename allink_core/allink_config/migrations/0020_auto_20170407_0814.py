# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0019_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkconfig',
            name='mask_icon_color',
            field=models.CharField(default='#282828', max_length=7, verbose_name='Mask icon color', help_text='Mask icon color for safari-pinned-tab.svg'),
        ),
        migrations.AlterField(
            model_name='allinkconfig',
            name='msapplication_tilecolor',
            field=models.CharField(default='#282828', max_length=7, verbose_name='msapplication TileColor', help_text='MS application TitleColor Field'),
        ),
        migrations.AlterField(
            model_name='allinkconfig',
            name='theme_color',
            field=models.CharField(default='#ffffff', max_length=7, verbose_name='Theme Color', help_text='Theme color for Android Chrome'),
        ),
    ]
