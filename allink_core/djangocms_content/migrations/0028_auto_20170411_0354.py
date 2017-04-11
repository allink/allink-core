# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0027_auto_20170407_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='anchor',
            field=models.CharField(verbose_name='ID', blank=True, max_length=255, help_text='ID of this content section which can be used for anchor reference from links.<br>Note: Only letters, numbers and hyphen. No spaces or special chars.'),
        ),
    ]
