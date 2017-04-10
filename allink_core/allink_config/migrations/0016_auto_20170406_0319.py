# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0015_allinkconfig_work_toolbar_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkconfig',
            name='blog_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='events_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='locations_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='members_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='news_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='people_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='testimonial_toolbar_enabled',
            field=models.BooleanField(default=True, verbose_name='Toolbar enabled?'),
        ),
    ]
