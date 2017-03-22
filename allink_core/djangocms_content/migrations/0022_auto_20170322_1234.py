# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0021_auto_20170321_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentcolumnplugin',
            name='title',
            field=models.CharField(max_length=255, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='template',
            field=models.CharField(help_text='Choose a template.', max_length=50, verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='title',
            field=models.CharField(help_text='The section title', max_length=255, null=True, verbose_name='Title', blank=True),
        ),
    ]
