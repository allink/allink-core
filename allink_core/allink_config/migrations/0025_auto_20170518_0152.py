# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0024_auto_20170518_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkconfig',
            name='mask_icon_color',
            field=models.CharField(blank=True, null=True, max_length=50, help_text='Mask icon color for safari-pinned-tab.svg', verbose_name='Mask icon color'),
        ),
        migrations.AlterField(
            model_name='allinkconfig',
            name='msapplication_tilecolor',
            field=models.CharField(blank=True, null=True, max_length=50, help_text='MS application TitleColor Field', verbose_name='msapplication TileColor'),
        ),
        migrations.AlterField(
            model_name='allinkconfig',
            name='theme_color',
            field=models.CharField(blank=True, null=True, max_length=50, help_text='Theme color for Android Chrome', verbose_name='Theme Color'),
        ),
    ]
