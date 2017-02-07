# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0003_auto_20170117_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='link_special',
            field=models.CharField(blank=True, max_length=255, verbose_name='Special Links', choices=[(b'member_login', 'Member Login'), (b'member_logout', 'Member Logout'), (b'member_reset_password', 'Member Change Passwort')]),
        ),
    ]
