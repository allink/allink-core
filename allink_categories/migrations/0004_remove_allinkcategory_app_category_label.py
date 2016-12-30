# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0003_auto_20161206_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkcategory',
            name='app_category_label',
        ),
    ]
