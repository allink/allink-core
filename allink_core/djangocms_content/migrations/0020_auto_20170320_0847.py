# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0019_allinkcontentplugin_project_css_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='project_css_classes',
            field=django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(max_length=50, null=True, blank=True), blank=True),
        ),
    ]
