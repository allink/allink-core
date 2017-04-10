# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0017_auto_20170406_0427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_special',
            field=models.CharField(max_length=255, null=True, choices=[('account_login', 'Member Login'), ('account_logout', 'Member Logout'), ('account_change_password', 'Member Change Passwort'), ('account_reset_password', 'Member Reset Passwort'), ('members:profile_edit', 'Member Edit Profile'), ('contact:request', 'Contact Form')], verbose_name='Special Links', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_url',
            field=models.URLField(default='', blank=True, verbose_name='External link', help_text='Provide a valid URL to an external website.'),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='ratio',
            field=models.CharField(max_length=50, null=True, verbose_name='Ratio', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='template',
            field=models.CharField(default=('default', 'Default'), max_length=50, choices=[('default', 'Default')], verbose_name='Template', help_text='Choose a template.'),
        ),
    ]
