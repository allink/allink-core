# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_socialicon', '0006_auto_20170321_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinksocialiconplugin',
            name='title',
            field=models.CharField(help_text='SEO text (not visible) e.g. Follow allink on Instagram', max_length=255, null=True, verbose_name='Title', blank=True),
        ),
    ]
