# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0006_auto_20160623_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Multicolumn',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_multicolumn_multicolumn', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('template', models.CharField(default=b'default', max_length=30, verbose_name='Template', choices=[(b'default', 'Standard'), (b'text-image', 'Bild mit Text'), (b'text-image-deco', 'Hintergrundbild mit Text')])),
                ('bg_image', filer.fields.image.FilerImageField(related_name='multicolumn', blank=True, to='filer.Image', help_text='Breite: 1300px', null=True, verbose_name='Hintergrundbild')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
