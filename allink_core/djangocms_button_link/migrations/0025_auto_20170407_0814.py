# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import allink_core.djangocms_button_link.model_fields
import allink_core.allink_base.models.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0024_auto_20170406_0427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkcontainerplugin',
            name='alignment_horizontal_desktop',
            field=models.CharField(null=True, blank=True, max_length=50, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], verbose_name='Alignment horizontal desktop', help_text='This option overrides the projects default alignment for desktop. (Usually "left")'),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkcontainerplugin',
            name='alignment_horizontal_mobile',
            field=models.CharField(null=True, blank=True, max_length=50, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], verbose_name='Alignment horizontal mobile', help_text='This option overrides the projects default alignment for mobile. (Usually "left")'),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='btn_context',
            field=allink_core.djangocms_button_link.model_fields.Context(default='default', max_length=255, choices=[('default', 'Default'), ('primary', 'Primary'), ('success', 'Success'), ('info', 'Info'), ('warning', 'Warning'), ('danger', 'Danger'), ('link', 'Link')], verbose_name='Context'),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='extra_css_classes',
            field=allink_core.allink_base.models.model_fields.Classes(default='', blank=True, verbose_name='Css Classes', help_text='Space separated classes that are added to the list of classes.'),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='icon_left',
            field=allink_core.allink_base.models.model_fields.Icon(default='', max_length=255, verbose_name='Icon left', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='icon_right',
            field=allink_core.allink_base.models.model_fields.Icon(default='', max_length=255, verbose_name='Icon right', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='label',
            field=models.CharField(default='', max_length=255, verbose_name='Display name', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_special',
            field=models.CharField(max_length=255, null=True, choices=[('account_login', 'Member Login'), ('account_logout', 'Member Logout'), ('account_change_password', 'Member Change Passwort'), ('account_reset_password', 'Member Reset Passwort'), ('members:profile_edit', 'Member Edit Profile'), ('contact:request', 'Contact Form')], verbose_name='Special Links', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_url',
            field=models.URLField(default='', blank=True, verbose_name='External link', help_text='Provide a valid URL to an external website.'),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='txt_context',
            field=allink_core.djangocms_button_link.model_fields.Context(default='', max_length=255, choices=[('', 'Default'), ('primary', 'Primary'), ('success', 'Success'), ('info', 'Info'), ('warning', 'Warning'), ('danger', 'Danger'), ('muted ', 'Muted')], verbose_name='Context', blank=True),
        ),
    ]
