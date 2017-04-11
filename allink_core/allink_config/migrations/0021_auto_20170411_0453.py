# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0020_auto_20170407_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkconfig',
            name='terms_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='terms_verbose',
            field=models.CharField(default='Terms of Service', max_length=255, verbose_name='Terms of Service verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='terms_verbose_plural',
            field=models.CharField(default='Terms of Service', max_length=255, verbose_name='Terms of Service verbose name plural'),
        ),
    ]
