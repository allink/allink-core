# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0012_auto_20170321_0415'),
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
        migrations.AlterField(
            model_name='allinkcategorytranslation',
            name='language_code',
            field=models.CharField(max_length=15, verbose_name='Language', db_index=True),
        ),
        migrations.AlterField(
            model_name='allinkcategorytranslation',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='name'),
        ),
    ]
