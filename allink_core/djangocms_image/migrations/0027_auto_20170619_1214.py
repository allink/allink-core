# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0026_auto_20170519_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_special',
            field=models.CharField(max_length=255, verbose_name='Special Links', null=True, blank=True),
        ),
    ]
