# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-13 11:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20170706_1647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactrequestplugin',
            old_name='internal_email_adresses',
            new_name='internal_email_addresses',
        ),
    ]