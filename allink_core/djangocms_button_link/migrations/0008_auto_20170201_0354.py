# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0007_auto_20170131_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='softpage_enabled',
            field=models.BooleanField(default=False, help_text='If checked, the content will be displayed in a "softpage". (Is currently only working with content of special links.))', verbose_name='Show in Softpage'),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_special',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Special Links', choices=[(b'account_login', 'Member Login'), (b'account_logout', 'Member Logout'), (b'account_change_password', 'Member Change Passwort'), (b'member:profile_edit', 'Member Edit Profile')]),
        ),
    ]
