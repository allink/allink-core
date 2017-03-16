# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0011_auto_20170309_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentcolumnplugin',
            name='order_mobile',
            field=models.IntegerField(help_text='Some columns should be ordered differently on mobile devices when columns are stacked vertically. This option allows you to define the position of the this column.<br><br>Note: Columns ordering is ascending (lowest number displayed first)', null=True, verbose_name='Order Mobile', blank=True),
        ),
    ]
