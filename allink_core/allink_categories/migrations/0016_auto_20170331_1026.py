# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0015_auto_20170330_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcategory',
            name='model_names',
            field=django.contrib.postgres.fields.ArrayField(help_text='Please specify the app which uses this categories. All apps specified in parent category are automatically added.', null=True, base_field=models.CharField(max_length=50), size=None, blank=True),
        ),
    ]
