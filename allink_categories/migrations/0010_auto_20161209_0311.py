# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0009_auto_20161207_0707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allinkcategory',
            old_name='app_label_categories',
            new_name='model_names',
        ),
    ]
