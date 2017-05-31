# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_instagram', '0004_auto_20170407_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkinstagramplugin',
            name='template',
            field=models.CharField(max_length=50, help_text='Choose a template.', verbose_name='Template'),
        ),
    ]
