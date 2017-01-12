# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0006_auto_20160623_1627'),
        ('allink_config', '0003_allinkconfig_default_og_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkMetaTagExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Title')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, to='filer.Image', help_text='Image when shared on Facebook.', null=True, verbose_name='og:Image')),
                ('public_extension', models.OneToOneField(related_name='draft_extension', null=True, editable=False, to='allink_config.AllinkMetaTagExtension')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
