# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0025_auto_20170407_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkbuttonlinkcontainerplugin',
            name='project_css_classes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, null=True, max_length=50), blank=True, null=True, size=None),
        ),
    ]
