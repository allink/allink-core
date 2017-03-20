# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0018_auto_20170315_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='project_css_classes',
            field=django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'test-class', b'Test Class')]), blank=True),
        ),
    ]
