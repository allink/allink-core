# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0008_allinkcategory_app_category_label'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allinkcategory',
            old_name='app_category_label',
            new_name='app_label_categories',
        ),
    ]
