# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0017_auto_20170406_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkconfig',
            name='events_registration_verbose',
            field=models.CharField(default='Event Registration', max_length=255, verbose_name='Events Registration verbose name'),
        ),
        migrations.AlterField(
            model_name='allinkconfig',
            name='events_registration_verbose_plural',
            field=models.CharField(default='Event Registrations', max_length=255, verbose_name='Events Registration verbose name plural'),
        ),
    ]
