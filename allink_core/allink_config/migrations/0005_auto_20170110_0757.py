# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0004_allinkmetatagextension'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkmetatagextension',
            name='og_description',
            field=models.CharField(help_text='Description when shared on Facebook.', max_length=255, null=True, verbose_name='og:description', blank=True),
        ),
        migrations.AddField(
            model_name='allinkmetatagextension',
            name='og_title',
            field=models.CharField(help_text='Title when shared on Facebook.', max_length=255, null=True, verbose_name='og:title', blank=True),
        ),
    ]
