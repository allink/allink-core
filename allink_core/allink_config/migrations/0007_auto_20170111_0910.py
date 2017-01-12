# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0006_allinkservicemenuextension'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkservicemenuextension',
            name='extended_object',
        ),
        migrations.RemoveField(
            model_name='allinkservicemenuextension',
            name='public_extension',
        ),
        migrations.DeleteModel(
            name='AllinkServiceMenuExtension',
        ),
    ]
