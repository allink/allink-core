# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0028_auto_20170823_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_special',
            field=models.CharField(max_length=255, blank=True, verbose_name='Form', null=True),
        ),
    ]
