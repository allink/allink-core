# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0014_allinkcategory_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcategory',
            name='tag',
            field=models.CharField(choices=[(b'locations', b'Locations')], max_length=80, blank=True, help_text='auto-generated categories use this tag, to identify which app generated the category.', null=True, verbose_name='Tag'),
        ),
    ]
