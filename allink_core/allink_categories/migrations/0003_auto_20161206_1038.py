# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0002_auto_20161206_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcategory',
            name='app_category_label',
            field=models.CharField(help_text='Please specify the app which uses this categories.', max_length=50, verbose_name='Project app'),
        ),
    ]