# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0028_auto_20170519_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='email_body_text',
            field=models.TextField(verbose_name='Body Text', blank=True, default=''),
        ),
        migrations.AddField(
            model_name='allinkbuttonlinkplugin',
            name='email_subject',
            field=models.CharField(verbose_name='Subject', blank=True, max_length=255, default=''),
        ),
    ]
