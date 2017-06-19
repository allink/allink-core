# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0029_auto_20170608_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_special',
            field=models.CharField(max_length=255, verbose_name='Special Links', null=True, blank=True),
        ),
    ]
