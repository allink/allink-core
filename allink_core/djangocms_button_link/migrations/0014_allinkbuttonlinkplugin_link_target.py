# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0013_auto_20170313_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='link_target',
            field=models.IntegerField(blank=True, null=True, verbose_name='Link Target', choices=[(1, 'New window'), (2, 'Softpage large'), (3, 'Softpage small'), (4, 'Lightbox (Forms)')]),
        ),
    ]