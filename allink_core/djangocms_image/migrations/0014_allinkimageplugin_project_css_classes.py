# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0013_allinkimageplugin_bg_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkimageplugin',
            name='project_css_classes',
            field=django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(max_length=50, null=True, blank=True), blank=True),
        ),
    ]
