# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0011_auto_20170317_0852'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allinkcategory',
            options={'verbose_name': 'Cat\xe9gorie', 'verbose_name_plural': 'Cat\xe9gories'},
        ),
        migrations.AlterModelOptions(
            name='allinkcategorytranslation',
            options={'default_permissions': (), 'verbose_name': 'Cat\xe9gorie Translation', 'managed': True},
        ),
        migrations.AlterField(
            model_name='allinkcategorytranslation',
            name='language_code',
            field=models.CharField(max_length=15, verbose_name='Langue', db_index=True),
        ),
        migrations.AlterField(
            model_name='allinkcategorytranslation',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='nom'),
        ),
    ]
