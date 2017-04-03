# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0016_auto_20170331_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcategory',
            name='tag',
            field=models.CharField(help_text='auto-generated categories use this tag, to identify which app generated the category.', max_length=80, null=True, verbose_name='Tag', blank=True),
        ),
    ]
