# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkLegacyLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('old', models.CharField(unique=True, max_length=255, verbose_name='Old Link')),
                ('new', models.CharField(max_length=255, verbose_name='New Link')),
                ('overwrite', models.CharField(help_text="Overwrites 'New Link', use for special urls that are not listed there", max_length=255, null=True, verbose_name='Overwrite Link', blank=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('match_subpages', models.BooleanField(default=False, help_text='If True, matches all subpages and redirects them to this link', verbose_name='Match subpages')),
                ('last_test_result', models.NullBooleanField(default=None, help_text='Was the last automatic test successfull? (True = Yes, False = No, None = Not yet tested)', verbose_name='Result of last test')),
                ('last_test_date', models.DateTimeField(null=True, verbose_name='Date of last test', blank=True)),
            ],
            options={
                'verbose_name': 'Legacy Link',
                'verbose_name_plural': 'Legacy Links',
            },
        ),
    ]
