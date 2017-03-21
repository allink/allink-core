# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_terms', '0005_allinktermsplugin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkterms',
            name='status',
            field=models.IntegerField(default=10, verbose_name='Status', choices=[(10, 'Draft'), (20, 'Publi\xe9'), (30, 'Archived')]),
        ),
        migrations.AlterField(
            model_name='allinktermstranslation',
            name='language_code',
            field=models.CharField(max_length=15, verbose_name='Langue', db_index=True),
        ),
    ]
