# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_terms', '0006_auto_20170321_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkterms',
            name='status',
            field=models.IntegerField(default=10, verbose_name='Status', choices=[(10, 'Draft'), (20, 'Published'), (30, 'Archived')]),
        ),
        migrations.AlterField(
            model_name='allinktermstranslation',
            name='language_code',
            field=models.CharField(max_length=15, verbose_name='Language', db_index=True),
        ),
    ]
