# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcategory',
            name='app_category_label',
            field=models.CharField(help_text='Please specify the app which uses this categories.', max_length=50, verbose_name='Project app', choices=[(0, b'course')]),
        ),
    ]
