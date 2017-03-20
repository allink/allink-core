# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0010_auto_20161209_0311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allinkcategory',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='allinkcategorytranslation',
            options={'default_permissions': (), 'verbose_name': 'Category Translation', 'managed': True},
        ),
    ]
