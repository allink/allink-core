# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0016_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkgalleryplugin',
            name='project_css_classes',
            field=django.contrib.postgres.fields.ArrayField(blank=True, null=True, size=None, base_field=models.CharField(blank=True, null=True, max_length=50)),
        ),
    ]
