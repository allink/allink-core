# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0009_auto_20170309_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcontentcolumnplugin',
            name='order_mobile',
            field=models.IntegerField(help_text='If some columns should be ordered different on mobile devices, this option allows you to so.', null=True, verbose_name='Order Mobile', blank=True),
        ),
    ]
