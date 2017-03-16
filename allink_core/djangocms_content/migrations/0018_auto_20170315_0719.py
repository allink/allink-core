# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0017_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='template',
            field=models.CharField(help_text='Choose a template.', max_length=50, verbose_name='Template'),
        ),
    ]
