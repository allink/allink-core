# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_terms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkterms',
            name='active',
        ),
        migrations.RemoveField(
            model_name='allinkterms',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='allinkterms',
            name='created',
        ),
        migrations.RemoveField(
            model_name='allinkterms',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='allinkterms',
            name='og_description',
        ),
        migrations.RemoveField(
            model_name='allinkterms',
            name='og_image',
        ),
        migrations.RemoveField(
            model_name='allinkterms',
            name='og_title',
        ),
    ]
