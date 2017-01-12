# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkconfig',
            name='google_tag_manager_id',
        ),
        migrations.RemoveField(
            model_name='allinkconfig',
            name='mailchimp_api_key',
        ),
        migrations.RemoveField(
            model_name='allinkconfig',
            name='mailchimp_list_id',
        ),
        migrations.RemoveField(
            model_name='allinkconfig',
            name='sentry_dns',
        ),
    ]
