# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0004_allinkbuttonlinkplugin_link_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_special',
            field=models.CharField(blank=True, max_length=255, verbose_name='Special Links', choices=[(b'member:login', 'Member Login'), (b'member:logout', 'Member Logout')]),
        ),
    ]
