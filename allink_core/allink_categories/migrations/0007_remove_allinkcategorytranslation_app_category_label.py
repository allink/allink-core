# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0006_auto_20161207_0305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkcategorytranslation',
            name='app_category_label',
        ),
    ]
