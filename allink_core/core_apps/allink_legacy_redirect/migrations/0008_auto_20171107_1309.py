# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-07 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0007_auto_20170714_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinklegacylink',
            name='language',
            field=models.CharField(choices=[('en', 'English')], default=('en', 'English'), max_length=200, null=True, verbose_name='Language'),
        ),
    ]