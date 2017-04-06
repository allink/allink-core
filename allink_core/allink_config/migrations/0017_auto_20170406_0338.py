# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0016_auto_20170406_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkconfig',
            name='contact_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='contact_verbose',
            field=models.CharField(default='Member', max_length=255, verbose_name='Contact verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='contact_verbose_plural',
            field=models.CharField(default='Members', max_length=255, verbose_name='Contact verbose name plural'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='events_registration_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='events_registration_verbose',
            field=models.CharField(default='Event', max_length=255, verbose_name='Events Registration verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='events_registration_verbose_plural',
            field=models.CharField(default='Events', max_length=255, verbose_name='Events Registration verbose name plural'),
        ),
    ]
