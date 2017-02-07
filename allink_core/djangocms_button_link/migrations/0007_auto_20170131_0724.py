# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0006_auto_20170131_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_special',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Special Links', choices=[(b'account_login', 'Member Login'), (b'account_logout', 'Member Logout')]),
        ),
    ]
