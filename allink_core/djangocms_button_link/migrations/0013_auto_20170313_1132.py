# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0012_auto_20170309_0224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allinkbuttonlinkplugin',
            old_name='link_target',
            new_name='link_target_old',
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_special',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Special Links', choices=[(b'account_login', 'Member Login'), (b'account_logout', 'Member Logout'), (b'account_change_password', 'Member Change Passwort'), (b'account_reset_password', 'Member Reset Passwort'), (b'members:profile_edit', 'Member Edit Profile'), (b'contact:request', 'Contact Form')]),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='softpage_enabled',
            field=models.BooleanField(default=False, help_text='If checked, the content will be displayed in a Softpage. (Is currently only working with content of special links.))', verbose_name='Show in Softpage'),
        ),
    ]
