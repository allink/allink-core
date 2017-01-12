# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_recipient', models.EmailField(max_length=254, null=True, verbose_name='Default recipient E-Mail', blank=True)),
                ('default_sender', models.EmailField(max_length=254, null=True, verbose_name='Default sender E-Mail', blank=True)),
                ('google_tag_manager_id', models.CharField(help_text='GTM-XXXX)', max_length=8, verbose_name='Google Tag Manager ID')),
                ('mailchimp_api_key', models.CharField(help_text='dd24567f941562fd4eb80167e7e56f20-us6)', max_length=36, verbose_name='Mailchimp API key')),
                ('mailchimp_list_id', models.CharField(help_text='eee2502457)', max_length=10, verbose_name='Mailchimp list ID')),
                ('sentry_dns', models.CharField(help_text='https://9d024cb19f62456898e438ebad1a45a4:a155bcce988247f68e8f785dc1122939@sentry.io/120253)', max_length=90, verbose_name='Sentry API key')),
            ],
            options={
                'verbose_name': 'Allink Configuration',
            },
        ),
    ]
