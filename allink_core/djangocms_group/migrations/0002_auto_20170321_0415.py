# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_group', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgroupcontainerplugin',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='allinkgroupplugin',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Titre'),
        ),
    ]
