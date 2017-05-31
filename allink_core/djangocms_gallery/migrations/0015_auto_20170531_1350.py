# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0014_auto_20170516_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgalleryplugin',
            name='template',
            field=models.CharField(max_length=50, help_text='Choose a template.', verbose_name='Template'),
        ),
    ]
